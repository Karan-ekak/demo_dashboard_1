"""  This dbx_file_address have the Folder Path in Dbx 

        parameter : Argus_id

        Role : Accessing File , Delete , Update - All CRUD Operation


"""


def dbx_attendanceCSV(argus_id):
    return '/Argus_Device/' + argus_id + '/attendanceCSV/'


def dbx_attendancePhotos(argus_id):
    return '/Argus_Device/' + argus_id + '/attendanceImages/'


def dbx_knownPersonalDatabaseCSV(argus_id):
    return '/Argus_Device/' + argus_id + '/knownPersonalDatabaseCSV/Total_knownPersonnelDatabase.csv'


def dbx_knownPersonalDatabasePhotos(argus_id):
    return '/Argus_Device/' + argus_id + '/knownPersonalDatabasePhotos/'


def dbx_unknownPhoto(argus_id):
    return '/Argus_Device/' + argus_id + '/UnknownPhotos/'


def dbx_status(argus_id):
    return '/Argus_Device/' + argus_id + '/Argus_Status/'

def dbx_report(argus_id):
    return '/Argus_Device/' + argus_id + '/reports/'