# Licensed under a 3-clause BSD style license - see LICENSE.rst


import pytest
import requests

from ...heasarc import Heasarc, Conf
from ...utils import commons


@pytest.mark.remote_data
class TestHeasarc:

    @property
    def isdc_context(self):
        return Conf.server.set_temp('https://www.isdc.unige.ch/browse/w3query.pl')

    def test_basic_example(self):
        mission = 'integral_rev3_scw'
        object_name = '3c273'

        heasarc = Heasarc()

        with self.isdc_context:
            table = heasarc.query_object(object_name, mission=mission, radius='1 degree')

        assert len(table) == 270

    def test_mission_list(self):
        heasarc = Heasarc()
        
        with self.isdc_context:
            missions = heasarc.query_mission_list()

        # Assert that there are indeed a large number of tables
        # Number of tables could change, but should be > 900 (currently 956)
        assert len(missions) == 5

    def test_mission_cols(self):
        heasarc = Heasarc()
        mission = 'integral_rev3_scw'

        with self.isdc_context:
            cols = heasarc.query_mission_cols(mission=mission)

        assert len(cols) == 35

        # Test that the cols list contains known names
        assert 'SCW_ID' in cols
        assert 'GOOD_ISGRI' in cols
        assert 'RA_X' in cols
        assert 'DEC_X' in cols
        assert '_SEARCH_OFFSET' in cols

    def test_query_object_async(self):
        mission = 'integral_rev3_scw'
        object_name = '3c273'

        heasarc = Heasarc()
        response = heasarc.query_object_async(object_name, mission=mission)
        assert response is not None
        assert type(response) is requests.models.Response

    def test_query_region_async(self):
        heasarc = Heasarc()
        mission = 'integral_rev3_scw'
        c = commons.coord.SkyCoord('12h29m06.70s +02d03m08.7s', frame='icrs')

        with self.isdc_context:
            response = heasarc.query_region_async(c, mission=mission,
                                                  radius='1 degree')
        assert response is not None
        assert type(response) is requests.models.Response

    #@pytest.mark.skip(reason="config is not passed correctly, for some reason?")
    def test_query_region(self):
        heasarc = Heasarc()
        mission = 'integral_rev3_scw'

        # Define coordinates for '3c273' object
        with self.isdc_context:
            c = commons.coord.SkyCoord('12h29m06.70s +02d03m08.7s', frame='icrs')
            table = heasarc.query_region(c, mission=mission, radius='1 degree')

        assert len(table) == 270
