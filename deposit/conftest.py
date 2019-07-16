import os
import pytest

from lxml import etree

from backend.conftest import load_test_data as papers_load_test_data

from deposit.models import DDC
from deposit.models import License

load_test_data = papers_load_test_data

@pytest.fixture()
def license_standard(db):
    """
    Returns a standard test license
    """

    license = License.objects.get_or_create(
        name="Standard License",
        uri="https://dissem.in/deposit/license/standard"
    )

    return license

@pytest.fixture()
def license_alternative(db):
    """
    Returns an alternative test license
    Use this license, if you need two of them
    """

    license = License.objects.get_or_create(
        name="Alternative License",
        uri="https://dissem.in/deposit/license/alternative"
    )

    return license


# This is a list of oairecords to be tested
metadata_publications = [
    'book-chapter_acute_interstitial_nephritis',
    'book-chapter_adaptive_multiagent_system_for_multisensor_maritime_surveillance',
    'book_god_of_the_labyrinth',
    'dataset_sexuality_assessment_in_older_adults_unique_situations',
    'journal-article_a_female_signal_reflects_mhc_genotype_in_a_social_primate',
    'journal-article_altes_und_neues_zum_strafrechtlichen_vorsatzbegriff',
    'journal-article_confrontation_with_heidegger',
    'journal-article_constructing_matrix_geometric_means',
    'journal-article_lobjet_de_la_dpression',
    'journal-issue_mode_und_gender',
    'other_assisting_configuration_based_feature_model_composition',
    'poster_development_of_new_gpe_conjugates_with_application_in_neurodegenerative_diseases',
    'preprint_nikomachische_ethik',
    'proceedings_sein_und_nichtsein',
    'proceedings-article_activitycentric_support_for_weaklystructured_business_processes',
    'proceedings-article_an_efficient_vofbased_rans_method_to_capture_complex_sea_states',
    'proceedings-article_cursos_efa',
    'reference-entry_chromatin_interaction_analysis_using_pairedend_tag_sequencing',
    'report_execution_of_targeted_experiments_to_inform_bison',
    'thesis_blue_mining_planung_des_abbaus_von_manganknollen_in_der_tiefsee',
]


@pytest.fixture(params=metadata_publications)
def upload_data(request, load_json):
    """
    Loads the above list of publications and returns form data the user has to fill in.
    """
    return load_json.load_upload(request.param)


@pytest.fixture(params=[True, False])
def ddc(request, db):
    """
    Run tests for protocol with repository having a DDC and not having a DDC
    """
    if request.param:
        all_ddc = DDC.objects.all()
        request.cls.protocol.repository.ddc.add(*all_ddc)
        return all_ddc
    else:
        return None


@pytest.fixture(scope="class")
def dissemin_xsd_1_0():
    '''
    Loads dissemin xsd and prepares it as schema ready for validation.
    '''

    testdir = os.path.dirname(os.path.abspath(__file__))
    dissemin_xsd = etree.parse(os.path.join(testdir, 'schema','dissemin_v1.0.xsd'))
    return etree.XMLSchema(dissemin_xsd)
