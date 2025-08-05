from datetime import datetime
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.business.load import (
    get_best_load,
    prioritize_loads,
)
from app.schemas.load import LoadFilter


class TestGetBestLoad:
    """Test suite for get_best_load function"""

    @patch("app.business.load.filter_loads_from_db")
    @patch("app.business.load.prioritize_loads")
    @patch("app.business.load.enrich_with_pricing")
    def test_get_best_load_strict_filters_success(
        self, mock_enrich, mock_prioritize, mock_filter
    ):
        """Test successful load retrieval with strict filters"""
        # Arrange
        mock_db = Mock(spec=Session)
        filters = LoadFilter(
            origin_city="Chicago", destination_city="Dallas", equipment_type="dry_van"
        )

        mock_load = Mock()
        mock_load.id = 1
        mock_filter.return_value = [mock_load]
        mock_prioritize.return_value = [mock_load]

        # Create a simple mock response instead of LoadResponse instance
        expected_response = Mock()
        expected_response.id = 1
        expected_response.first_offer = 2500
        expected_response.max_rate = 3000
        expected_response.rate_per_mile = 2.5
        mock_enrich.return_value = expected_response

        # Act
        result = get_best_load(mock_db, filters)

        # Assert
        assert result == expected_response
        mock_filter.assert_called_once_with(mock_db, filters)
        mock_prioritize.assert_called_once_with([mock_load])
        mock_enrich.assert_called_once_with(mock_load)

    @patch("app.business.load.filter_loads_from_db")
    @patch("app.core.config.constants")
    def test_get_best_load_fallback_to_relaxed_filters(
        self, mock_constants, mock_filter
    ):
        """Test fallback to relaxed filters when strict filters return no results"""
        # Arrange
        mock_db = Mock(spec=Session)
        filters = LoadFilter(
            origin_city="Chicago", destination_city="Dallas", equipment_type="dry_van"
        )

        mock_constants.RELAXED_FILTER_FIELDS = {
            "miles": None,
            "delivery_datetime": None,
        }

        # First call returns empty, second call returns results
        mock_load = Mock()
        mock_filter.side_effect = [[], [mock_load]]

        with patch("app.business.load.prioritize_loads") as mock_prioritize, patch(
            "app.business.load.enrich_with_pricing"
        ) as mock_enrich:
            mock_prioritize.return_value = [mock_load]
            mock_enrich.return_value = Mock()

            # Act
            result = get_best_load(mock_db, filters)

            # Assert
            assert result is not None
            assert mock_filter.call_count == 2
            # First call with original filters
            mock_filter.assert_any_call(mock_db, filters)
            # Second call should be with relaxed filters

    @patch("app.business.load.filter_loads_from_db")
    def test_get_best_load_no_results(self, mock_filter):
        """Test when no loads are found even with relaxed filters"""
        # Arrange
        mock_db = Mock(spec=Session)
        filters = LoadFilter(origin_city="NonExistentCity")

        # Both strict and relaxed filters return empty
        mock_filter.return_value = []

        # Act
        result = get_best_load(mock_db, filters)

        # Assert
        assert result is None


class TestPrioritizeLoads:
    """Test suite for prioritize_loads function"""

    def test_prioritize_loads_urgent_first(self):
        """Test that urgent loads are prioritized first"""
        # Arrange
        regular_load = Mock()
        regular_load.notes = "Standard delivery"
        regular_load.delivery_datetime = datetime(2025, 8, 10, 12, 0)

        urgent_load = Mock()
        urgent_load.notes = "URGENT delivery needed"
        urgent_load.delivery_datetime = datetime(
            2025, 8, 12, 12, 0
        )  # Later date but urgent

        loads = [regular_load, urgent_load]

        with patch("app.core.config.constants") as mock_constants:
            mock_constants.URGENT_KEYWORD = "urgent"
            mock_constants.FALLBACK_DELIVERY_DATETIME = datetime(2099, 12, 31)

            # Act
            result = prioritize_loads(loads)

            # Assert
            assert result[0] == urgent_load  # Urgent load should be first
            assert result[1] == regular_load

    def test_prioritize_loads_by_delivery_date(self):
        """Test prioritization by delivery date when urgency is same"""
        # Arrange
        later_load = Mock()
        later_load.notes = "Regular delivery"
        later_load.delivery_datetime = datetime(2025, 8, 15, 12, 0)

        earlier_load = Mock()
        earlier_load.notes = "Standard delivery"
        earlier_load.delivery_datetime = datetime(2025, 8, 10, 12, 0)

        loads = [later_load, earlier_load]

        with patch("app.core.config.constants") as mock_constants:
            mock_constants.URGENT_KEYWORD = "urgent"
            mock_constants.FALLBACK_DELIVERY_DATETIME = datetime(2099, 12, 31)

            # Act
            result = prioritize_loads(loads)

            # Assert
            assert result[0] == earlier_load  # Earlier delivery should be first
            assert result[1] == later_load

    def test_prioritize_loads_handles_none_notes(self):
        """Test that loads with None notes are handled properly"""
        # Arrange
        load_with_none_notes = Mock()
        load_with_none_notes.notes = None
        load_with_none_notes.delivery_datetime = datetime(2025, 8, 10, 12, 0)

        load_with_notes = Mock()
        load_with_notes.notes = "Has notes"
        load_with_notes.delivery_datetime = datetime(2025, 8, 11, 12, 0)

        loads = [load_with_notes, load_with_none_notes]

        with patch("app.core.config.constants") as mock_constants:
            mock_constants.URGENT_KEYWORD = "urgent"
            mock_constants.FALLBACK_DELIVERY_DATETIME = datetime(2099, 12, 31)

            # Act
            result = prioritize_loads(loads)

            # Assert
            assert len(result) == 2
            assert result[0] == load_with_none_notes  # Earlier delivery date
