def set_renderpath():
    final = os.path.join(get_1st_lvl())
    final = final.replace("2_Work", "3_Output")
    print('final: ', final)
    return(final)