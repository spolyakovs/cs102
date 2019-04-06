import unittest
import os
import multiprocess


pool = multiprocess.Pool()


class TestMultiprocess(unittest.TestCase):

    def test_get_proc_memory(self):
        #TODO: поймать исключение
        pass

    def test_map(self):
        # can not test this function
        pass

    def test_check_workers_count(self):

        self.assertRaises(Exception, pool.check_workers_count, 1)

        self.assertEqual(pool.check_workers_count(2), 2)

        self.assertEqual(pool.check_workers_count(5), 5)

        self.assertEqual(pool.check_workers_count(10), 10)

        self.assertEqual(pool.check_workers_count(20), 10)

    def test_start_first_worker(self):
        #TODO: поймать исключение
        pass

    def test_init_worker(self):
        # can not test this function
        pass

    def test_first_worker_func(self):
        pool.input_q.put((3, 7))
        pool.first_worker_func(lambda x, y: x + y)

        self.assertEqual(pool.output_q.get(), str(10) + " by worker " + str(os.getpid()))

    def test_worker_func(self):
        pool.input_q.put((3, 7))
        pool.input_q.put((4321, 1234))
        pool.input_q.put((0, 0))
        pool.worker_func(lambda x, y: x + y)

        self.assertEqual(pool.output_q.get(), str(10) + " by worker " + str(os.getpid()))
        self.assertEqual(pool.output_q.get(), str(5555) + " by worker " + str(os.getpid()))
        self.assertEqual(pool.output_q.get(), str(0) + " by worker " + str(os.getpid()))


if __name__ == '__main__':
    unittest.main()
