"""
This program simulates a two-level page table and Translation Lookaside Buffer (TLB) to explore virtual-to-physical address translation.
It demonstrates TLB hits, TLB misses, and page faults using various access patterns.
Author: Rahul Kumar
Date: November 25, 2024
"""

import random
from collections import OrderedDict

# Constants
PAGE_TABLE_LEVEL_1_SIZE = 4  # Number of entries in Level 1 Page Table
PAGE_TABLE_LEVEL_2_SIZE = 4  # Number of entries in Level 2 Page Table
FRAME_SIZE = 256             # Size of each frame in bytes
TLB_SIZE = 8                 # Number of entries in the TLB cache

# Bit masks and shifts for extracting parts of the virtual address
LEVEL_1_BITS = 2             # Number of bits for Level 1 index (4 entries -> 2 bits)
LEVEL_2_BITS = 2             # Number of bits for Level 2 index (4 entries -> 2 bits)
OFFSET_BITS = 8              # Number of bits for offset (256 bytes -> 8 bits)

LEVEL_1_MASK = (1 << LEVEL_1_BITS) - 1
LEVEL_2_MASK = (1 << LEVEL_2_BITS) - 1
OFFSET_MASK = (1 << OFFSET_BITS) - 1

# Simulated Two-Level Page Table (randomly generated)
page_table = {i: {j: random.randint(0, 15) for j in range(
    PAGE_TABLE_LEVEL_2_SIZE)} for i in range(PAGE_TABLE_LEVEL_1_SIZE)}

# Simulated TLB (Translation Lookaside Buffer) using OrderedDict for LRU
tlb = OrderedDict()

# Function to translate a virtual address to a physical address using bit manipulation
def translate_address(virtual_address) -> tuple:
    """
    Translate a virtual address to a physical address using a two-level page table and TLB.
    Returns a tuple with the physical address and a boolean indicating if it was a TLB hit.
    """
    # Extract Level 1 index, Level 2 index, and offset from the virtual address
    level_1_index = (virtual_address >> (LEVEL_2_BITS + OFFSET_BITS)) & LEVEL_1_MASK
    # TODO-1: Level 2 index, and Offset using bit manipulation. In the next two lines, replace the None values with the correct bit manipulation code
    level_2_index = (virtual_address >> OFFSET_BITS) & LEVEL_2_MASK
    offset = virtual_address & OFFSET_MASK

    # Initialize physical address and TLB hit flag
    physical_address = None
    is_tlb_hit = False

    # Check if the virtual page is in the TLB
    if (level_1_index, level_2_index) in tlb:
        # TODO-2: TLB hit: Retrieve the physical frame from the TLB
        physical_frame = tlb[(level_1_index, level_2_index)]
        # Update TLB for LRU by moving the accessed item to the end
        tlb.move_to_end((level_1_index, level_2_index))
        print(f"TLB hit for virtual page ({level_1_index}, {level_2_index}).")

        # TODO-2.1: Calculate the physical address using the frame number and offset
        physical_address = (physical_frame << OFFSET_BITS) | offset
        # TODO-2.2: Set the is_tlb_hit flag to True
        is_tlb_hit = True

    # If not in the TLB, check the page table
    elif level_1_index in page_table and level_2_index in page_table[level_1_index]:
        # TODO-3: TLB miss: Retrieve the physical frame from the two-level page table
        physical_frame = page_table[level_1_index][level_2_index]
        # Add the entry to the TLB
        tlb[(level_1_index, level_2_index)] = physical_frame
        print(f"TLB miss. Retrieved from page table for virtual page ({level_1_index}, {level_2_index}).")

        # TODO-4: If the TLB is full, evict the least recently used entry
        if len(tlb) > TLB_SIZE:
            evicted_page = tlb.popitem(last=False)
            print(f"Evicted page {evicted_page} from TLB (LRU policy).")

        # TODO-4.1: Calculate the physical address using the frame number and offset
        physical_address = (physical_frame << OFFSET_BITS) | offset
        # TODO-4.2: Set the is_tlb_hit flag to False
        is_tlb_hit = False

    # If not in the page table, it's a page fault
    else:
        print(f"Page fault! Virtual page ({level_1_index}, {level_2_index}) is not in page table.")

    return physical_address, is_tlb_hit

# Function to simulate address access patterns and calculate TLB performance
def simulate_address_access(access_pattern):
    """
    Simulate address translation for a given access pattern and calculate TLB hit rate.
    """
    tlb_hits = 0
    tlb_misses = 0

    for virtual_address in access_pattern:
        # Translate the virtual address to a physical address
        physical_address, was_tlb_hit = translate_address(virtual_address)
        if was_tlb_hit:
            tlb_hits += 1
        else:
            tlb_misses += 1

    # Calculate and print the TLB hit rate
    print("\nSimulation Results:")
    print(f"Total Accesses: {len(access_pattern)}")
    print(f"TLB Hits: {tlb_hits}")
    print(f"TLB Misses: {tlb_misses}")
    # TODO-5: Calculate and print the TLB hit rate
    hit_rate = (tlb_hits / len(access_pattern)) * 100 if len(access_pattern) > 0 else 0
    print(f"TLB Hit Rate: {hit_rate:.2f}%")

# Main function to run multiple test cases with different access patterns
def main():
    print("Test Case 1: Sequential Access Pattern")
    sequential_access_pattern = list(range(
        0, PAGE_TABLE_LEVEL_1_SIZE * PAGE_TABLE_LEVEL_2_SIZE * FRAME_SIZE, FRAME_SIZE))
    simulate_address_access(sequential_access_pattern)

    print("\nTest Case 2: Random Access Pattern")
    random_access_pattern = [random.randint(
        0, PAGE_TABLE_LEVEL_1_SIZE * PAGE_TABLE_LEVEL_2_SIZE * FRAME_SIZE - 1) for _ in range(50)]
    simulate_address_access(random_access_pattern)

    print("\nTest Case 3: Repeated Access to Small Subset")
    repeated_access_pattern = [0, FRAME_SIZE, 2 *
                               FRAME_SIZE, 0, FRAME_SIZE, 2 * FRAME_SIZE] * 5
    simulate_address_access(repeated_access_pattern)

# Run the main function
if __name__ == "__main__":
    main()
