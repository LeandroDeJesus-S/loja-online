import pytest
from django.core.exceptions import ValidationError

from mediafiles.models import MediaFile
from utils.support.messages import MediaFileMessages


def test_media_file_str_method_with_sigle_fks(
        memory_upload_img_file,
        product_variation,
        processing_order_evaluation
    ):
    """test if the return of the __str__ method is correct
    when sending just one fk by time.
    """
    mf = MediaFile(
        file=memory_upload_img_file,
        evaluation=processing_order_evaluation,
    )

    ev = f"Avaliação: {mf.evaluation} arquivo: {mf.file.name}"

    assert str(mf) == ev
    
    mf.evaluation = None
    mf.product_variation = product_variation
    pdt = f"Produto: {mf.product_variation} arquivo: {mf.file.name}"
    assert str(mf) == pdt



def test_media_file_str_method_with_both_fks(
    memory_upload_img_file,
    product_variation,
    processing_order_evaluation
):
    """test if the __str__ method raises exception when both
    fks are given.
    """
    mf = MediaFile(
        file=memory_upload_img_file,
        evaluation=processing_order_evaluation,
        product_variation=product_variation,
    )
    with pytest.raises(Exception) as e:
        str(mf)
    
    assert e.value.args[0] == MediaFileMessages.INVALID_FK_SENT


def test_media_file_chk_mediafile_fks_not_given_together_constraint_fails(
    memory_upload_img_file,
    product_variation,
    processing_order_evaluation
):
    """test the model chk_mediafile_fks_not_given_together constraint fail cases"""
    mf = MediaFile(
        file=memory_upload_img_file,
        evaluation=processing_order_evaluation,
        product_variation=product_variation,
    )
    with pytest.raises(ValidationError) as e:
        mf.validate_constraints()
    
    assert e.match(str(MediaFileMessages.INVALID_FK_SENT))

    mf.product_variation = None
    mf.evaluation = None

    with pytest.raises(ValidationError) as e:
        mf.validate_constraints()
    
    assert e.match(str(MediaFileMessages.INVALID_FK_SENT))


def test_media_file_chk_mediafile_fks_not_given_together_constraint_succes(
    memory_upload_img_file,
    product_variation,
    processing_order_evaluation
):
    """test the model chk_mediafile_fks_not_given_together constraint success cases"""
    mf = MediaFile(
        file=memory_upload_img_file,
        evaluation=processing_order_evaluation,
    )
    try:
        mf.validate_constraints()
    except ValidationError:
        pytest.fail('ValidationError raised to evaluation')

    mf.evaluation = None
    mf.product_variation = product_variation

    try:
        mf.validate_constraints()
    except ValidationError:
        pytest.fail('ValidationError raised product_variation')
