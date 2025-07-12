"""Purpose is this file `Department and Their Sub Department Logic`
    - We Can Access and Perform Operation on Department and Their Sub Department Logic 

"""

from database_connection import ArgusDB


def list_department() -> tuple:

    contractor = (
        (0, 'Raw Material Processing'),
        (1, 'Raw Material Handling'),
        (2, 'Raw Material Storage'),
        (3, 'Security'),
        (4, 'Manufacturing'),
        (5, 'QA / QC'),
        (6, 'Packaging'),
        (7, 'Product Storage'),
        (8, 'Product Loading'),
        (9, 'Product Handling'),
        (10, 'Parking'),
        (11, 'Common Area (Tandeli) '),
        (12, 'Boiler Room'),
        (13, 'Canteen'),
        (14, 'Admin'),
    )
    return contractor


def list_sub_department(id_zero=0) -> dict:
    sub_contractor = {
        0: {
            'total': id_zero,
            'low': 0,
            'medium': 0,
            'high': id_zero
        },
        # 1: {
        #     'total': 89,
        #     'low': 34,
        #     'medium': 13,
        #     'high': 42
        # },
        # 2: {
        #     'total': 55,
        #     'low': 18,
        #     'medium': 22,
        #     'high': 15
        # },
        # 3: {
        #     'total': 34,
        #     'low': 11,
        #     'medium': 16,
        #     'high': 7
        # },
        # 4: {
        #     'total': 21,
        #     'low': 7,
        #     'medium': 8,
        #     'high': 6
        # },
        # 5: {
        #     'total': 13,
        #     'low': 4,
        #     'medium': 5,
        #     'high': 4
        # },
    }
    # query = f'''SELECT
    #         COUNT(*) AS total_entries,
    #         SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS count_status_id_1,
    #         SUM(CASE WHEN status = 2 THEN 1 ELSE 0 END) AS count_status_id_3,
    #         SUM(CASE WHEN status = 3 THEN 1 ELSE 0 END) AS count_status_id_5
    #         FROM argus."1005_incident";'''
    try:
        pass
        # incident_total = ArgusDB().get_query(query)
        # # print(incident_total)
        # front_val = {
        #     'total': incident_total[0],
        #     'low': incident_total[1],
        #     'medium': incident_total[2],
        #     'high': incident_total[3],
        # }
        # sub_contractor[1] = front_val
    except Exception as Err:
        print(f"Error {Err}")
    return sub_contractor

def sub_department(id,static_data=0):
    try:
        
        id = int(id)
        if id == 1:
            query=F'''   SELECT mid,count(*) FROM argus."1005_incident"
                    Group BY mid
                    Order by mid desc
                '''
            dataSD=ArgusDB().get_all(query=query)
            # print(dataSD)

            data_sub_department={
                    1:{
                        'Sorting Belt 1':[ dataSD[0][0],dataSD[0][1]-50,dataSD[0][1]+80,dataSD[0][1]-30 ],
                        'ETP Area':[dataSD[1][0],dataSD[1][1]-50,dataSD[1][1]+80,dataSD[1][1]-30],
                        'Feading M/C':[dataSD[2][0],dataSD[2][1]-50,dataSD[2][1]+80,dataSD[2][1]-30],
                        'Sorting Belt 2':[dataSD[3][0],dataSD[3][1]-50,dataSD[3][1]+80,dataSD[3][1]-30],
                        'Carestic Tank 1':[dataSD[4][0],dataSD[4][1]-50,dataSD[4][1]+80,dataSD[4][1]-30],
                        'Carestic Tank 2':[dataSD[5][0],dataSD[5][1]-50,dataSD[5][1]+80,dataSD[5][1]-30],
                    }
                }
            return data_sub_department[1]
    
        data_sub_department={
            0:{
                'Wash Feeding M/C 1no line':[1,0,static_data,0],
            },
            2:{
                'Packing Area':[1,11,21,11],
                'Maintaince Area':[1,12,13,9],
                'Back Area 1':[1,13,12,13],
                'Power Control Area':[1,14,8,9],                  
            },
            3:{
                'Godown 1':[1,12,42,3],
                'Packing Area':[1,17,15,13],
                'Loading Area':[1,21,6,8],
                'Godown 2':[2,21,2,13],
            },
            4:{
                'Godown 3':[1,9,3,1],
                'Winding  Dhaga 1':[1,2,3,6],
                'Dye House':[1,1,2,3],
                'Dispatch Area':[1,5,4,2],
            },
            5:{
                'Front Area':[1,1,3,1],
                'Rafiya':[1,0,2,3],
                'Cotton House':[1,2,2,1],
                'Diesel Tank':[1,2,1,2],
            }
        }
        
        if id in data_sub_department:
            return data_sub_department[id]
    except Exception as Err:
        print(f'Error {Err}')
    return {}


if __name__ == '__main__':
    pass
