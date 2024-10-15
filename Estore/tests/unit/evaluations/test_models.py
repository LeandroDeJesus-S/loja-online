from evaluations.models import Evaluation


def test_evaluation_str_method(processing_order):
    """test the return of the __str__ method"""
    e = Evaluation(
        evaluation=Evaluation.BAD,
        description='not good',
        order=processing_order,
    )
    expected = f'{e.order.user} - {e.order} | {e.evaluation}'

    assert str(e) == expected
