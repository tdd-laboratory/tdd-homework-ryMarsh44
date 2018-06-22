import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # 2
    def test_correctly_extracts_date(self):
        self.assert_extract("I was born on 2018-07-25.", library.dates_iso8601, "2018-07-25")

    # 6
    def test_not_extract_invalid_data(self):
        self.assert_extract("I was born on 2017-17-25.", library.dates_iso8601)

    # 8
    def test_correctly_extracts_data_with_month(self):
        self.assert_extract("25 Jan 2017", library.dates_fmt2)

    # Rest of tests

    def test_time_stamp_z(self):
        self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.123Z', library.dates_iso8601, '2018-06-22T18:22:19.123Z')

    def test_time_stamp(self):
        self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.123', library.dates_iso8601,
                            '2018-06-22T18:22:19.123')

    def test_time_stamp_t(self):
        self.assert_extract("something 2018-12-25T18:22:19.12", library.dates_iso8601, '2018-12-25 18:22:19.12')

    def test_date_with_comma(self):
        self.assert_extract('I have 123,456,789', library.integers)

    def test_data_with_abb_month(self):
        self.assert_extract('Current date is 25 Jan. 2017', library.dates_fmt2)

    def test_data_with_comma_month(self):
        self.assert_extract('Current date is 25 Jan, 2017', library.dates_fmt2)

    def test_dates_with_offset(self):
        self.assert_extract("2018-12-25T18:22:19.12 -0800", library.dates_iso8601, '2018-12-25 10:22:19.12')

    def test_dates_UTC(self):
        self.assert_extract("2018-12-25 18:22:19.12 UTC", library.dates_iso8601, '2018-12-25 10:22:19.12')

    def test_time_stamp_mdt(self):
        self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.123MDT', library.dates_iso8601,
                            '2018-06-22T18:22:19.123MDT')

    def test_time_stamp_mst(self):
        self.assert_extract('Current timeStamp is 2018-06-22T18:22:19.123MST', library.dates_iso8601,
                            '2018-06-22T18:22:19.123MST')


if __name__ == '__main__':
    unittest.main()
