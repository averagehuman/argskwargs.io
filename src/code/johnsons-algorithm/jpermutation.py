#!/usr/bin/env python3
        
        
def jpermute(iterable):
    """
    Use the Johnson-Trotter algorithm to return all permutations of iterable.
    """
    sequence = list(iterable)
    length = len(sequence)
    indices = range(1, length+1)
    # the list of directed integers: [-1, 1], [-1, 2], ...
    state = [[-1, idx] for idx in indices]
    # add sentinels at the beginning and end
    state = [[-1, length+1]] + state + [[-1, length+1]]
    # the first permutation is the sequence itself
    yield sequence
    mobile_index = mobile_direction = direction = value = None
    while True:
        # 1. find the highest mobile
        mobile = -1
        for idx in indices:
            direction, value = state[idx]
            if value > mobile and value > state[idx+direction][1]:
                # value is mobile and greater than the previous mobile
                mobile = value
                mobile_index = idx
                mobile_direction = direction
                if mobile == length:
                    # no point in continuing as mobile is as large as it can be.
                    break
        if mobile == -1:
            break
        
        # 2. swap the mobile with the element it 'sees'
        sees = mobile_index + mobile_direction
        state[mobile_index], state[sees] = state[sees], state[mobile_index]
        sequence[mobile_index-1], sequence[sees-1] = sequence[sees-1], sequence[mobile_index-1]
        
        # 3. switch the direction of elements greater than mobile
        if mobile < length:
            for idx in indices:
                if state[idx][1] > mobile:
                    state[idx][0] = -state[idx][0]
        yield sequence
 
if __name__ == '__main__':
    for perm in jpermute('ABCD'):
        print(perm)