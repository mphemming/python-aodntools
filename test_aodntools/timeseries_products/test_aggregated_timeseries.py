import os
import unittest

from netCDF4 import Dataset

from test_aodntools.base_test import BaseTestCase
from aodntools.timeseries_products.aggregated_timeseries import main_aggregator


TEST_ROOT = os.path.dirname(__file__)
BAD_FILE = 'IMOS_ANMN-NRS_TZ_20181213T080000Z_NRSROT_FV00_NRSROT-1812-SBE39-43_END-20181214T004000Z_C-20190827T000000Z.nc'
INPUT_FILES = [
    'IMOS_ANMN-NRS_BCKOSTUZ_20181213T080038Z_NRSROT_FV01_NRSROT-1812-WQM-55_END-20181215T013118Z_C-20190828T000000Z.nc',
    'IMOS_ANMN-NRS_TZ_20181213T080000Z_NRSROT_FV01_NRSROT-1812-SBE39-23_END-20190306T160000Z_C-20190827T000000Z.nc',
    'IMOS_ANMN-NRS_TZ_20190313T144000Z_NRSROT_FV01_NRSROT-1903-SBE39-27_END-20190524T010000Z_C-20190827T000000Z.nc',
    BAD_FILE
]
INPUT_PATHS = [os.path.join(TEST_ROOT, f) for f in INPUT_FILES]


class TestAggregatedTimeseries(BaseTestCase):
    def test_main_aggregator(self):
        output_file, bad_files = main_aggregator(INPUT_PATHS, 'TEMP', 'NRSROT', self.temp_dir)

        self.assertEqual(1, len(bad_files))
        for path, errors in bad_files.items():
            self.assertEqual(os.path.join(TEST_ROOT, BAD_FILE), path)
            self.assertSetEqual(set(errors), {'no NOMINAL_DEPTH', 'Wrong file version: Level 0 - Raw Data'})

        dataset = Dataset(output_file)
        self.assertSetEqual(set(dataset.dimensions), {'OBSERVATION', 'INSTRUMENT', 'string256'})
        self.assertSetEqual(set(dataset.variables.keys()),
                            {'TIME', 'LATITUDE', 'LONGITUDE', 'NOMINAL_DEPTH', 'DEPTH', 'DEPTH_quality_control',
                             'PRES', 'PRES_quality_control', 'PRES_REL', 'PRES_REL_quality_control',
                             'TEMP', 'TEMP_quality_control', 'instrument_index', 'instrument_id', 'source_file'}
                            )

        obs_vars = {'TIME', 'DEPTH', 'DEPTH_quality_control', 'PRES', 'PRES_quality_control',
                    'PRES_REL', 'PRES_REL_quality_control', 'TEMP', 'TEMP_quality_control', 'instrument_index'}
        for var in obs_vars:
            self.assertEqual(dataset.variables[var].dimensions, ('OBSERVATION',))


if __name__ == '__main__':
    unittest.main()