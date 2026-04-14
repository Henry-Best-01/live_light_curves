'''utility file'''



def parse_arguments(all_arguments=None):
    '''this function takes the list of arguments provided and generates a
    dictionaryfrom them if possible'''

    if all_arguments == []:
        return None, []

    list_of_targets = all_arguments.pop(0)
    if len(list_of_targets) > 0:    
        other_args = all_arguments
    else:
        other_args = None
        
    if all_arguments is None:
        print("please provide a list or json of targets to monitor")
        print("include the path to target coordinates as a json or csv file")
        print("these can be generated using the 'SLED_lenses.py' script provided")

    elif list_of_targets[-4:] == 'json':
        import json
        with open(list_of_targets, 'r') as f:
            current_targets = json.load(f)

    elif list_of_targets[-3:] == 'csv':
        import csv
        current_targets = []
        with open(list_of_targets, 'r') as f:
            my_reader = csv.DictReader(f)
            for row in my_reader:
                current_targets.append(row)
    else:
        print("list of objects not recognized. please provide a valid json or csv.")
        print("these can be generated using the 'SLED_lenses.py' script provided")
        return list_of_targets, all_arguments
    return current_targets, other_args


def open_tap_service(
    home_directory='~',
    rsp_tap_token_filename='.rsp-tap.token',
):
    '''opens the RSP TAP service'''
    import pyvo
    import os 
    RSP_TAP_SERVICE = 'https://data.lsst.cloud/api/tap'
    homedir = os.path.expanduser(home_directory)
    token_file = os.path.join(homedir, rsp_tap_token_filename)
    with open(token_file, 'r') as f:
        token_str = f.readline()
    cred = pyvo.auth.CredentialStore()
    cred.set_password("x-oauth-basic", token_str)
    credential = cred.get("ivo://ivoa.net/sso#BasicAA")
    rsp_tap = pyvo.dal.TAPService(RSP_TAP_SERVICE, session=credential)
    return rsp_tap


def prepare_butler(
    configuration='dp1',
    collections='LSSTComCam/DP1'
):
    '''prepare the lsst Butler required to get image data'''
    from lsst.daf.butler import Butler

    ### requires fix
    butler = Butler() #configuration, collections=collections)
    assert butler is not None
    return butler



def query_coords(butler, band, ra, dec, time_last):
    '''checks a given set of coordinates if there is a new visit image'''
    query = f"band.name = '{band}' AND visit_detector_region.region OVERLAPS POINT ({ra}, {dec})"
    


    # get data at coordinates provided (add list support)
    pass

def processed_stellar_cutouts():
    # use Lightcurver or other method
    pass







def send_alert():
    # send out alerts as defined
    pass

def update_web_page():
    # update the monitoring page
    pass












