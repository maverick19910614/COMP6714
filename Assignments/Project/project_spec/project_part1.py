def sortByDID(posting):
    a = []
    re1 = []
    re = dict()
    for i,j in posting.items():
        if j[0]!=0:
            a.append((j[0],i))
    for i in sorted(a):
        re[i[1]] = posting[i[1]]
        re1.append(i[1])
    return re,re1

def sort_answer(answer):
    d = dict()
    for i in range(len(answer)):
        d[answer[i][0]] = []
    for i in range(len(answer)):
        d[answer[i][0]].append(i)
    d_key = sorted(d)
    d_key.reverse()
    new_d = dict()
    for i in d_key:
        new_d[i] = d[i]
    e = []
    for i,j in new_d.items():
        e.extend(answer[j[0]:j[-1]+1])
    return e

def preprocessing(query_items, inverted_index):
    key_list = []
    for i in range(len(query_items)):
        if query_items[i] not in key_list:
            key_list.append(query_items[i])
        else:
            t = 1
            b = query_items[i]
            while query_items[i] in key_list:
                query_items[i] = query_items[i] + str(t)
                t += 1
            key_list.append(query_items[i])
            inverted_index[query_items[i]] = inverted_index[b]
    return query_items, inverted_index

# def WAND_Algo(query_terms, top_k, inverted_index):
#     evaluation_count = 0
#     q_len = len(query_terms)
#     uper_bound = dict()
#     postings = dict()
#     d_num = 0
#     for i in query_terms:
#         uper_bound[i] = max([j[1] for j in inverted_index[i]])
#         postings[i] = inverted_index[i][d_num]
#         (ct, wt) = inverted_index[i][d_num]
#     threshold = 0
#     answer = []
#     while (ct, wt) != (0, 0):
#         evaluation_count += 1
#         sorted_p, sorted_t = sortByDID(postings)
#         print(sorted_p)
#         q_len = len(sorted_t)
#         score_limit = 0
#         pivot = 0
#         while pivot < q_len - 1:
#             tmp_s_lim = score_limit + uper_bound[sorted_t[pivot]]
#             if tmp_s_lim > threshold:
#                 break
#             score_limit = tmp_s_lim
#             pivot = pivot + 1
#         # print(pivot,score_limit,sorted_p,sorted_t)
#
#         if sorted_p[sorted_t[0]][0] == sorted_p[sorted_t[pivot]][0]:
#             s = 0
#             t = 0
#             d_num += 1
#             while t < q_len and sorted_p[sorted_t[t]][0] == sorted_p[sorted_t[pivot]][0]:
#                 s = s + sorted_p[sorted_t[t]][1]
#                 # d_num += 1
#                 if d_num <= len(inverted_index[sorted_t[t]]) - 1:
#                     # print(d_num,sorted_t[t],inverted_index[sorted_t[t]][1])
#                     postings[sorted_t[t]] = inverted_index[sorted_t[t]][d_num]
#                     # print(posting)
#                     (ct, wt) = inverted_index[sorted_t[t]][d_num]
#                 else:
#                     postings[sorted_t[t]] = (0, 0)
#                     (ct, wt) = (0, 0)
#                 t = t + 1
#             if s > threshold:
#                 #                 if
#                 answer.append((s, sorted_p[sorted_t[pivot]][0]))
#                 # print(answer)
#                 if len(answer) > top_k:
#                     answer = sorted(answer)
#                     d_list = [i[0] for i in answer]
#                     min_num = 0
#                     for i in d_list:
#                         if i == min(d_list):
#                             min_num += 1
#                     if min_num > 1 and answer[min_num-2][0] == answer[min_num-1][0]:
#                         answer.remove(answer[min_num-1])
#                     else:
#                         answer.remove(answer[0])
#
#                     # answer = sorted(answer)[-top_k:]
#         #             print(answer)
#         #                     inverted_answer = [(i[1],i[0]) for i in answer][-top_k:]
#         #                     threshold = inverted_answer[0][0]
#         #                     answer = [(i[1],i[0]) for i in inverted_answer]
#         else:
#             for i in range(pivot):
#                 judge = 0
#                 for j in inverted_index[sorted_t[i]]:
#                     if j[0] >= pivot:
#                         postings[sorted_t[i]] = j
#                         (ct, wt) = j
#                         judege = 1
#                         break
#                 if judge == 0:
#                     postings[sorted_t[i]] = (0, 0)
#                     (ct, wt) = (0, 0)
#     answer = sort_answer(answer)
#
#     return answer, evaluation_count
    #pass ## Replace this line with your implementation...!




def WAND_Algo(query_terms, top_k, inverted_index):
    query_terms, inverted_index = preprocessing(query_terms, inverted_index)
    evaluation_count = 0
    q_len = len(query_terms)
    uper_bound = dict()
    postings = dict()
    # d_num = 0
    posting_index = dict()
    for i in query_terms:
        posting_index[i] = 0
        uper_bound[i] = max([j[1] for j in inverted_index[i]])
        postings[i] = inverted_index[i][posting_index[i]]
        (ct, wt) = inverted_index[i][posting_index[i]]
    threshold = 0
    answer = []
    tt = 0
    while (ct, wt) != (0, 0):
        tt = 0
        for i,j in postings.items():
            if j != (0,0):
                tt = 1
        if tt == 0:
            break
        # print(postings)
        # evaluation_count += 1
        if tt == 1:
            sorted_p, sorted_t = sortByDID(postings)
            q_len = len(sorted_t)
        # print('sorted_p',sorted_p)
        # # print(evaluation_count)
        # # print('threshold',threshold)
        # # print(posting_index)
        # # print(sorted_t)
        # print(ct,wt)

        #print(q_len)
        score_limit = 0
        pivot = 0
        full = 0
        if q_len == 1 and uper_bound[sorted_t[pivot]] > threshold:
            evaluation_count += 1
        while pivot < q_len - 1:

            tmp_s_lim = score_limit + uper_bound[sorted_t[pivot]]
            # if q_len == 3:
            #     print(tmp_s_lim)
            #     print(uper_bound[sorted_t[pivot]])
            if tmp_s_lim > threshold:

                # print(12345)
                # print('answer',answer)
                # print('threshold', threshold)
                # print(sorted_p)
                # print('evaluation_count',evaluation_count)

                #print(2222)
                full = 1
                #evaluation_count += 1
                break
            if pivot == q_len-2:

                tmp_s_lim = tmp_s_lim + uper_bound[sorted_t[pivot+1]]
                if tmp_s_lim > threshold:
                    full = 1
                    pivot = pivot + 1
                    break

            score_limit = tmp_s_lim
            pivot = pivot + 1

        # print(pivot,score_limit,sorted_p,sorted_t)

        if sorted_p[sorted_t[0]][0] == sorted_p[sorted_t[pivot]][0]:
            if full == 1:
                evaluation_count += 1
                # print('postings',postings)
            #print(111111)
            s = 0
            t = 0
            #d_num += 1
            while t < q_len and sorted_p[sorted_t[t]][0] == sorted_p[sorted_t[pivot]][0]:

                s = s + sorted_p[sorted_t[t]][1]
                posting_index[sorted_t[t]] += 1
                # d_num += 1
                if posting_index[sorted_t[t]] <= len(inverted_index[sorted_t[t]]) - 1:
                    # print(d_num,sorted_t[t],inverted_index[sorted_t[t]][1])
                    postings[sorted_t[t]] = inverted_index[sorted_t[t]][posting_index[sorted_t[t]]]
                    # print(postings)
                    (ct, wt) = inverted_index[sorted_t[t]][posting_index[sorted_t[t]]]
                else:
                    # print(sorted_t[t])
                    # print(111)
                    postings[sorted_t[t]] = (0, 0)
                    #(ct, wt) = (0, 0)
                t = t + 1
            # print('posting_index',posting_index)
            # print(sorted_p)
            if s > threshold:
                #evaluation_count += 1
                #                 if
                answer.append((s, sorted_p[sorted_t[pivot]][0]))
                #print(answer)
                # print(answer)
                #                 if len(answer) > top_k:
                #                     answer = sorted(answer)
                #                     if answer[0][0] == answer[1][0]:
                #                         answer.remove(answer[1])
                #                     else:
                #                         answer.remove(answer[0])
                if len(answer) > top_k:

                    answer = sorted(answer)
                    d_list = [i[0] for i in answer]
                    min_num = 0
                    for i in d_list:
                        if i == min(d_list):
                            min_num += 1
                    if min_num > 1 and answer[min_num - 2][0] == answer[min_num - 1][0]:
                        answer.remove(answer[min_num - 1])
                    else:
                        answer.remove(answer[0])
                    threshold = answer[0][0]
                    #print(1111111)
                    # answer = sorted(answer)[-top_k:]
        #             print(answer)
        #                     inverted_answer = [(i[1],i[0]) for i in answer][-top_k:]
        #                     threshold = inverted_answer[0][0]
        #                     answer = [(i[1],i[0]) for i in inverted_answer]
        else:
            # print('s',postings)
            # print(posting_index)
            # print('pivot',pivot)
            for i in range(pivot):
                judge = 0
                for j in inverted_index[sorted_t[i]]:
                    # print(inverted_index[sorted_t[i]])
                    # posting_index[sorted_t[i]] += 1
                    # print(j)
                    # print(j[0])
                    # print('c_pivot',sorted_p[sorted_t[pivot]][0])
                    # print(pivot)
                    if j[0] >= sorted_p[sorted_t[pivot]][0]:
                        posting_index[sorted_t[i]] = inverted_index[sorted_t[i]].index(j)
                        postings[sorted_t[i]] = j
                        (ct, wt) = j
                        judge = 1
                        break
                if judge == 0:
                    postings[sorted_t[i]] = (0,0)
                    # print(1111111111122)
                    #(ct, wt) = (0, 0)
            # print('e',postings)
            # print(posting_index)
        #print(ct)
    answer = sort_answer(answer)
    return answer, evaluation_count


# def WAND_Algo(query_terms, top_k, inverted_index):
#     evaluation_count = 0
#     q_len = len(query_terms)
#     uper_bound = dict()
#     postings = dict()
#     # d_num = 0
#     posting_index = dict()
#     for i in query_terms:
#         posting_index[i] = 0
#         uper_bound[i] = max([j[1] for j in inverted_index[i]])
#         postings[i] = inverted_index[i][posting_index[i]]
#         (ct, wt) = inverted_index[i][posting_index[i]]
#     threshold = 0
#     answer = []
#     tt = 0
#     while (ct, wt) != (0, 0):
#         tt = 0
#         for i,j in postings.items():
#             if j != (0,0):
#                 tt = 1
#         if tt == 0:
#             break
#         # print(postings)
#         # evaluation_count += 1
#         if tt == 1:
#             sorted_p, sorted_t = sortByDID(postings)
#             q_len = len(sorted_t)
#         # print('sorted_p',sorted_p)
#         # # print(evaluation_count)
#         # # print('threshold',threshold)
#         # # print(posting_index)
#         # # print(sorted_t)
#         # print(ct,wt)
#
#         #print(q_len)
#         score_limit = 0
#         pivot = 0
#         full = 0
#         if q_len == 1 and uper_bound[sorted_t[pivot]] > threshold:
#             evaluation_count += 1
#         while pivot < q_len - 1:
#
#             tmp_s_lim = score_limit + uper_bound[sorted_t[pivot]]
#             # if q_len == 3:
#             #     print(tmp_s_lim)
#             #     print(uper_bound[sorted_t[pivot]])
#             if tmp_s_lim > threshold:
#
#                 # print(12345)
#                 # print('answer',answer)
#                 # print('threshold', threshold)
#                 # print(sorted_p)
#                 # print('evaluation_count',evaluation_count)
#
#                 #print(2222)
#                 full = 1
#                 #evaluation_count += 1
#                 break
#             if pivot == q_len-2:
#
#                 tmp_s_lim = tmp_s_lim + uper_bound[sorted_t[pivot+1]]
#                 if tmp_s_lim > threshold:
#                     full = 1
#                     pivot = pivot + 1
#                     break
#
#             score_limit = tmp_s_lim
#             pivot = pivot + 1
#
#         # print(pivot,score_limit,sorted_p,sorted_t)
#
#         if sorted_p[sorted_t[0]][0] == sorted_p[sorted_t[pivot]][0]:
#             if full == 1:
#                 evaluation_count += 1
#                 # print('postings',postings)
#             #print(111111)
#             s = 0
#             t = 0
#             #d_num += 1
#             while t < q_len and sorted_p[sorted_t[t]][0] == sorted_p[sorted_t[pivot]][0]:
#
#                 s = s + sorted_p[sorted_t[t]][1]
#                 posting_index[sorted_t[t]] += 1
#                 # d_num += 1
#                 if posting_index[sorted_t[t]] <= len(inverted_index[sorted_t[t]]) - 1:
#                     # print(d_num,sorted_t[t],inverted_index[sorted_t[t]][1])
#                     postings[sorted_t[t]] = inverted_index[sorted_t[t]][posting_index[sorted_t[t]]]
#                     # print(postings)
#                     (ct, wt) = inverted_index[sorted_t[t]][posting_index[sorted_t[t]]]
#                 else:
#                     # print(sorted_t[t])
#                     # print(111)
#                     postings[sorted_t[t]] = (0, 0)
#                     #(ct, wt) = (0, 0)
#                 t = t + 1
#             # print('posting_index',posting_index)
#             # print(sorted_p)
#             if s > threshold:
#                 #evaluation_count += 1
#                 #                 if
#                 answer.append((s, sorted_p[sorted_t[pivot]][0]))
#                 #print(answer)
#                 # print(answer)
#                 #                 if len(answer) > top_k:
#                 #                     answer = sorted(answer)
#                 #                     if answer[0][0] == answer[1][0]:
#                 #                         answer.remove(answer[1])
#                 #                     else:
#                 #                         answer.remove(answer[0])
#                 if len(answer) > top_k:
#
#                     answer = sorted(answer)
#                     d_list = [i[0] for i in answer]
#                     min_num = 0
#                     for i in d_list:
#                         if i == min(d_list):
#                             min_num += 1
#                     if min_num > 1 and answer[min_num - 2][0] == answer[min_num - 1][0]:
#                         answer.remove(answer[min_num - 1])
#                     else:
#                         answer.remove(answer[0])
#                     threshold = answer[0][0]
#                     #print(1111111)
#                     # answer = sorted(answer)[-top_k:]
#         #             print(answer)
#         #                     inverted_answer = [(i[1],i[0]) for i in answer][-top_k:]
#         #                     threshold = inverted_answer[0][0]
#         #                     answer = [(i[1],i[0]) for i in inverted_answer]
#         else:
#             # print('s',postings)
#             # print(posting_index)
#             # print('pivot',pivot)
#             for i in range(pivot):
#                 judge = 0
#                 for j in inverted_index[sorted_t[i]]:
#                     # print(inverted_index[sorted_t[i]])
#                     # posting_index[sorted_t[i]] += 1
#                     # print(j)
#                     # print(j[0])
#                     # print('c_pivot',sorted_p[sorted_t[pivot]][0])
#                     # print(pivot)
#                     if j[0] >= sorted_p[sorted_t[pivot]][0]:
#                         posting_index[sorted_t[i]] = inverted_index[sorted_t[i]].index(j)
#                         postings[sorted_t[i]] = j
#                         (ct, wt) = j
#                         judge = 1
#                         break
#                 if judge == 0:
#                     postings[sorted_t[i]] = (0,0)
#                     # print(1111111111122)
#                     #(ct, wt) = (0, 0)
#             # print('e',postings)
#             # print(posting_index)
#         #print(ct)
#     answer = sort_answer(answer)
#     return answer, evaluation_count
