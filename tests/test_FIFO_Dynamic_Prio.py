import unittest
import sys
import os

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from FIFO_Dynamic_Prio import FIFO_Dynamic_Prio

class TestFIFO_Dynamic_Prio(unittest.TestCase):

    def setUp(self):
        """Create a new FIFO_Dynamic_Prio instance before each test."""
        self.fifo = FIFO_Dynamic_Prio(5)

    def test_serve(self):
        """Test serving when nothing is queued."""
        valid, next_serve = self.fifo.next_serve()
        self.assertFalse(valid)  # Nothing queued so should not be possible

    def test_enqueue(self):
        """Test that after enqueuing, the correct object is served."""
        self.fifo.enqueue_object("MC1")
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC1")  # First in queue should be MC1

    def test_enqueue_multiple(self):
        """Test that after enqueuing multiple objects, the correct one is served."""
        self.fifo.enqueue_object("MC1")
        self.fifo.enqueue_object("MC2")
        self.fifo.enqueue_object("MC3")
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC1")  # First in queue should be MC1

    def test_prioritise_one_with_priority(self):
        """Test that prioritising an object affects serving order."""
        self.fifo.enqueue_object("MC1")
        self.fifo.enqueue_object("MC2")
        self.fifo.prioritise_object("MC2", 2)  # Higher priority for MC2
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC2")  # MC2 has priority value assigned

    def test_prioritise_both_with_priority(self):
        """Test that prioritising both objects affects serving order."""
        self.fifo.enqueue_object("MC1")
        self.fifo.prioritise_object("MC2", 1)  # Higher priority for MC2
        self.fifo.enqueue_object("MC2")
        self.fifo.prioritise_object("MC2", 2)  # Higher priority for MC2
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC2")  # MC2 has highest priority

    def test_dequeue(self):
        """Test dequeuing an object."""
        self.fifo.enqueue_object("MC1")
        self.fifo.dequeue_object("MC1")
        valid, next_serve = self.fifo.next_serve()
        self.assertFalse(valid)  # Queue should be empty

    def test_dequeue_multiple(self):
        """Test dequeuing from multiple enqueued objects."""
        self.fifo.enqueue_object("MC1")
        self.fifo.enqueue_object("MC2")
        self.fifo.dequeue_object("MC1")
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC2")  # Next should be MC2

    def test_dequeue_prio(self):
        """Test dequeuing a prioritized object."""
        self.fifo.enqueue_object("MC1")
        self.fifo.prioritise_object("MC1")
        self.fifo.dequeue_object("MC1")
        valid, next_serve = self.fifo.next_serve()
        self.assertFalse(valid)  # Queue should be empty

    def test_dequeue_prio_multiple(self):
        """Test dequeuing from a queue with prioritized objects."""
        self.fifo.enqueue_object("MC1")
        self.fifo.prioritise_object("MC1")
        self.fifo.enqueue_object("MC2")
        self.fifo.prioritise_object("MC2")
        self.fifo.dequeue_object("MC1")
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC2")  # Next should be MC2

    def test_deprioritise(self):
        """Test that deprioritising an object affects serving order."""
        self.fifo.enqueue_object("MC1")
        self.fifo.prioritise_object("MC1")
        self.fifo.deprioritise_object("MC1")
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC1")  # MC1 should still be served

    def test_deprioritise_multiple(self):
        """Test deprioritising from a queue with multiple objects."""
        self.fifo.enqueue_object("MC1")
        self.fifo.prioritise_object("MC1")
        self.fifo.enqueue_object("MC2")
        self.fifo.prioritise_object("MC2")
        self.fifo.deprioritise_object("MC1")
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC2")  # Next should be MC2

    def test_empty_queue_after_multiple_dequeues(self):
        """Test that the queue is empty after multiple dequeues."""
        self.fifo.enqueue_object("MC1")
        self.fifo.enqueue_object("MC2")
        self.fifo.dequeue_object("MC1")
        self.fifo.dequeue_object("MC2")
        valid, next_serve = self.fifo.next_serve()
        self.assertFalse(valid)  # Queue should be empty

    def test_enqueue_to_full_queue(self):
        """Test enqueuing to a full queue without raising an error."""
        # Enqueue the maximum allowed objects in the queue
        self.fifo.enqueue_object("MC1")
        self.fifo.enqueue_object("MC2")
        self.fifo.enqueue_object("MC3")
        self.fifo.enqueue_object("MC4")
        self.fifo.enqueue_object("MC5")  # Queue should now be full

        # Attempting to enqueue an additional object (MC6) should be ignored
        self.fifo.enqueue_object("MC6")  # This should not raise an error or change the queue

        # Now we check the next object to serve
        valid, next_serve = self.fifo.next_serve()
        
        # The queue is still valid and should serve the first object (MC1)
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC1")  # MC1 should still be the next to serve


    def test_serving_order_with_mixed_priorities(self):
        """Test that serving order respects priorities."""
        self.fifo.enqueue_object("MC1")
        self.fifo.prioritise_object("MC1", 1)  # Low priority
        self.fifo.enqueue_object("MC2")
        self.fifo.prioritise_object("MC2", 2)  # Higher priority
        self.fifo.enqueue_object("MC3")
        self.fifo.prioritise_object("MC3", 3)  # Highest priority

        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC3")  # Should serve MC3 first
        
        serve = self.fifo.serve()
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC2")  # Next should be MC2

    def test_dequeue_nonexistent_object(self):
        """Test dequeuing a nonexistent object."""
        self.fifo.enqueue_object("MC1")
        self.fifo.dequeue_object("MC2")  # Should raise an error since MC2 is not in the queue
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC1")  # Next should be MC1

    def test_prioritise_nonexistent_object(self):
        """Test prioritising a nonexistent object."""
        self.fifo.enqueue_object("MC1")
        self.fifo.prioritise_object("MC2", 1)  # Should raise an error since MC2 is not in the queue
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC1")  # Next should be MC1

    def test_multiple_prioritizations(self):
        """Test multiple prioritizations on the same object."""
        self.fifo.enqueue_object("MC1")
        self.fifo.enqueue_object("MC2")
        self.fifo.prioritise_object("MC1", 2)
        self.fifo.prioritise_object("MC2", 1)  # Higher priority again
        self.fifo.prioritise_object("MC2", 3)  # Higher priority again
        valid, next_serve = self.fifo.next_serve()
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC1")  # Should still serve MC1

    def test_multiple_prioritizations(self):
        """Test multiple prioritizations on the same object."""
        # Enqueue two objects into the queue
        self.fifo.enqueue_object("MC1")
        self.fifo.enqueue_object("MC2")
        
        # Assign a priority to MC1
        self.fifo.prioritise_object("MC1", 2)
        
        # Assign priorities to MC2, which are higher than MC1's
        self.fifo.prioritise_object("MC2", 1)  # Higher priority for MC2
        self.fifo.prioritise_object("MC2", 3)  # Even higher priority for MC2

        # Now check which object is next to serve
        valid, next_serve = self.fifo.next_serve()
        
        # Depending on your prioritization logic, the following might change
        # If MC2's priority is indeed higher than MC1's, we expect it to be served next
        self.assertTrue(valid)
        self.assertEqual(next_serve, "MC2")  # Expecting MC2 to be served due to higher priority

    def tearDown(self):
        """Clean up after each test if necessary."""
        pass

if __name__ == '__main__':
    unittest.main()
