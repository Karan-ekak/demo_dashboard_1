# from database_connection import ArgusDB
# def oee_calculate_Data():
#    ''' OEE Calculation starts here '''
#     defect = total_defects_today or 0
#     material = total_material_count or 0
#     idle_time_minutes = parse_idle_time_to_minutes(idle_time)
    
#     quality = (1 - (defect / (defect + material))) * 100 if (defect + material) > 0 else 0
#     performance_efficiency = ((material + defect) / 17940) * 100 if 17940 > 0 else 0   # 17940 = scheduled pieces
#     availability = (1350 - idle_time_minutes - 90) / 1350 * 100                        # 1350 = Planned production time
#     overall_efficiency = quality*performance_efficiency*availability / 10000
    


#     table_name_analysis = "1007_OEE"
#     print("table_name_analysis : ",table_name_analysis)
#     key_value ={
       
#         'quality' : quality,
#         'performance' : performance_efficiency,
#         'availibility' : availability,
#         'oee' :overall_efficiency
#     }
#     status_insertion = ArgusDB().insert_db(table_name=table_name_analysis,Key_values=key_value)

#     return {
#         "quality": round(quality, 2),
#         "performance": round(performance_efficiency, 2),
#         "availability": round(availability, 2),
#         "oee": round(overall_efficiency, 2)
#     }