from Modules.que import Priority_Que

def test_priority_queue():
    pq = Priority_Que(evaluation_func=lambda x: x)
    pq.push(2)
    pq.push(4)
    pq.push(-5)

    assert pq.pop() == -5
    assert pq.pop() == 2
    assert pq.pop() == 4

def test_inverted_priority_queue():
    pq = Priority_Que(evaluation_func=lambda x: -x)
    pq.push(2)
    pq.push(4)
    pq.push(-5)

    assert pq.pop() == 4
    assert pq.pop() == 2
    assert pq.pop() == -5