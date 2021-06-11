import requests

#FIXIT

def calc_age(uid):
    r = requests.get(
        f'https://api.vk.com/method/friends.get?v=5.71&access_token=807910f0807910f0807910f0678001150b88079807910f0e0c9d4092cd02dfef407e8ed&user_id={uid}&fields=bdate')
    data = r.json()['response']['items']

    result = list()
    for i in range(len(data)):
        date = data[i].get('bdate', '')
        if len(date) > 5:
            result.append(2021 - int(date[-4:]))

    ans = list()
    ans.append([result[0], 1])
    for i in range(1, len(result)):
        for j in range(len(ans)):

            if result[i] == ans[j][0]:
                ans[j][1] += 1
                break
        else:

            ans.append([result[i], 1])

    ans = sorted(ans, key=lambda student: student[1], reverse=True)
    for j in range(len(ans)):
        for i in range(len(ans)-1):
            if ans[i][1] == ans[i+1][1] and ans[i][0] > ans[i+1][0]:
                ans[i],ans[i+1] = ans[i+1], ans[i]

    for i in range(len(ans)):
        ans[i] = tuple(ans[i])
    return ans



if __name__ == '__main__':
    res = calc_age('209584238')
