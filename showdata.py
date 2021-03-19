import pymysql
import matplotlib.pyplot as plt
import re
import numpy as np

conn = pymysql.connect(host="localhost",
                       user='root',
                       password='Sunsetgo@123',
                       db = 'uniranking',)


c = conn.cursor()

def get_uniname():
    temp_list = []
    uni_names = []
    uniname = input("请输入大学名称：")
    for year in range(2004,2019):
        table_name = "ARWU" + str(year)
        select_data = "SELECT * FROM " + table_name + " WHERE `UNINAME` LIKE %s"
        c.execute(select_data, ("%" + uniname +"%"))
        result = list(c.fetchall())
        for data in result:
            temp_list.append(data[2])
    for name in temp_list:
        if name not in uni_names:
            uni_names.append(name)
    if len(uni_names) > 0:
        i = 1
        for name in uni_names:
            print(str(i) + " - " + name)
            i += 1
        try:
            selected_uni = input("请输入选中的数字来选择大学: ")
            return_value = uni_names[int(selected_uni) - 1]
        except ValueError:
            print("输入有误...")
            get_uniname()
        else:
            return return_value

    else:
        print("这所学校不在排名中...")
        get_uniname()

def plot_graph(uniname):
    uni_data = {}
    for year in range(2004,2019):
        table_name = "ARWU" + str(year)
        select_data = "SELECT * FROM " + table_name + " WHERE `UNINAME` LIKE %s"
        c.execute(select_data, ("%" + uniname + "%"))
        result = c.fetchone()
        if result is not None:
            uni_data[str(year)] = list(result)

    x_data = list(uni_data.keys())
    rank_data = []
    total_score_data = []
    alumini_score_data = []
    award_score_data = []
    hiciscore_score_data = []
    ns_score_data = []
    pub_score_data = []
    pcp_score_data = []


    for data in uni_data.values():
        rank_data.append(get_mean_rank_number(data))
        total_score_data.append(data[3])
        alumini_score_data.append(data[4])
        award_score_data .append(data[5])
        hiciscore_score_data.append(data[6])
        ns_score_data.append(data[7])
        pub_score_data.append(data[8])
        pcp_score_data.append(data[9])


    plt.figure()
    ax = plt.gca()
    plt.title("World rank of " + uniname)
    plt.xlabel("year")
    ax.invert_yaxis()
    plt.plot(x_data, rank_data, color="#ff9696", linewidth=2.0,linestyle='-')


    plt.figure()
    plt.title("Score of " + uniname)
    plt.xlabel("year")
    plt.ylabel("Score")
    plt.ylim(0,100)
    plt.plot(x_data, alumini_score_data, color="blue", linewidth=1.0, linestyle='--', label="Alumini")
    plt.plot(x_data, ns_score_data, color="green", linewidth=1.0, linestyle=':', label='N&S')
    plt.plot(x_data, award_score_data, color="red", linewidth=1.0, linestyle='-', label='Award')
    plt.plot(x_data, hiciscore_score_data, color="yellow", linewidth=1.0, linestyle='--', label='HICI')
    plt.plot(x_data, pub_score_data, color="black", linewidth=1.0, linestyle=':', label='PUB')
    plt.plot(x_data, pcp_score_data, color="orange", linewidth=1.0, linestyle='-.', label='PCP')
    plt.legend()
    plt.show()



def get_mean_rank_number(data):
    rank_number = []
    rank_numbers = re.findall('\d+', data[1])
    for number in rank_numbers:
        rank_number.append(int(number))
    mean_number = int(np.mean(rank_number))

    return mean_number

plot_graph(get_uniname())

conn.close()