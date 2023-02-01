"""
Author: Xinran Zhang
SID: 500671702
Unikey: xzha0459
"""

import sys
from datetime import datetime


def is_valid_name(name):
    is_string = isinstance(name, str)
    if not is_string:
        return False
    elif name.replace(' ', '') == "":
        return False
    else:
        this_name = name.strip().replace(" ", "").replace("-", "")
        result = this_name.isalpha()
        if name.replace('-', '') == "":
            result = True
        return result



def is_valid_score(score):
    try:
        n = float(score)
        if n.is_integer() and str(score).count('.') == 0:
            score = int(score)
            if score < -10 or score > 10:
                result = False
            else:
                result = True
    except :
        result = False   
    return result



def is_valid_date(datetime):
    is_string = isinstance(datetime, str)
    if not is_string:
        return False
    else:
        try:
            date, time = datetime.split("T")
            year, month, date = date.split("-")
            hour, minute, second = time.split(":")
            result = False
            length = len(year)==4 and len(month)==2 and len(date)==2 and len(hour)==2 and len(minute)==2 and len(second)==2 
            is_digit = year.isdigit() and month.isdigit() and date.isdigit() and hour.isdigit() and minute.isdigit() and second.isdigit()
            if length == True and is_digit == True:
                result = True
        except:
            result=False
        return result



def is_chronological(earlier_datetime, later_datetime):
    format_pattern = '%Y-%m-%dT%H:%M:%S'
    a = datetime.strptime(later_datetime, format_pattern)
    b = datetime.strptime(earlier_datetime, format_pattern)
    if a > b:
        result = True
    else:
        result = False
    return result
            


def rank_people(people_file, log_file):
    log = open(log_file,"w")
    people = open(people_file,"r")
    people_content = people.readlines()

    # check if file headers are valid
    first_header = people_content[0].replace("\n","")
    second_header = people_content[1].replace("\n","")
    if first_header == "" or second_header != "":
        print("Error: people file read. The people file header is incorrectly formatted",file=log)
        sys.exit()
    
    new_file = people_content[0] + people_content[1]

    h = 2
    scores = []
    while h < len(people_content):
        try:
            name, score = people_content[h].split(",")
            score = score.strip()
        except ValueError:
            print(f"Error: people file read. The people entry is invalid on line {h+1}",file=log)
            sys.exit()
        
        if not is_valid_name(name):
            print(f"Error: people file read. The user's name is invalid on line {h+1}",file=log)
            sys.exit()

        if not is_valid_score(score):
            print(f"Error: people file read. The personality score is invalid on line {h+1}",file=log)
            sys.exit()

        scores.append([int(score), len(people_content)-h, name])
        h += 1

    scores.sort(reverse = True)

    m = 0
    while m < len(scores):
        new_scores = scores[m]
        new_file = new_file + f"{new_scores[2]},{new_scores[0]}\n"
        m += 1

    people.close()
    people = open(people_file,"w")
    new_people = people.write(new_file)
    people.close()
    log.close()



def validate_forum(forum_file, log_file):
    log = open(log_file,"w")
    forum = open(forum_file,"r")
    forum_content = forum.readlines()

    first_header = forum_content[0].replace("\n","")
    second_header = forum_content[1].replace("\n","")
    if first_header == "" or second_header != "":
        print("Error: forum file read. The forum file header is incorrectly formatted",file=log)
        sys.exit()

    post_already = False # whether there is a post before this line
    is_posting = True # whether this line is in a post
    is_reply = False # whether this line is in a reply
    
    dates = []
    dates_post = []

    i = 2
    while i < len(forum_content):
        content = forum_content[i]

        # check the format of forum file
        if content[0] == "\t":
            if not post_already:
                if i == 2:
                    print(f"Error: forum file read. The reply is placed before a post on line {i+1}",file=log)
                    sys.exit()
            if is_posting and (i+2)%3==2:
                print(f"Error: forum file read. The reply is placed before a post on line {(i+1)//3*3}",file=log)
                sys.exit()
            is_reply = True
        else:
            if is_reply:
                print(f"Error: forum file read. The post has an invalid format on line {(i+1)//3*3}",file=log)
                sys.exit()
        
        # check date
        if (i-2)%3 == 0:
            if not is_valid_date(content.strip().replace("\t","")):
                print(f"Error: forum file read. The datetime string is invalid on line {i+1}",file=log)
                sys.exit()
            if len(dates) == 0: # the first date
                dates.append(content.strip().replace("\t",""))
                dates_post.append(content.strip())
            else:
                if content[0] == "\t": 
                    # compare every reply with the post/reply before it
                    if not is_chronological(dates[-1], content.strip().replace("\t","")):
                        print(f"Error: forum file read. The reply is out of chronological order on line {i+1}",file=log)
                        sys.exit()
                    dates.append(content.strip().replace("\t",""))
                else:
                    # compare every post with the post before it
                    if not is_chronological(dates_post[-1], content.strip()):
                        print(f"Error: forum file read. The post is out of chronological order on line {i+1}",file=log)
                        sys.exit()
                    dates.append(content.strip().replace("\t",""))
                    dates_post.append(content.strip())
        #check name
        elif (i-2)%3 == 1:
            if not is_valid_name(content.strip().replace("\t","")):
                print(f"Error: forum file read. The user's name is invalid on line {i+1}",file=log)
                sys.exit()
        # check message and change bool
        elif (i-2)%3 == 2:
            if post_already == False:
                post_already = True
                is_posting = False
            if is_reply == True:
                is_reply = False
        i += 1
        
    forum.close()
    log.close()



def validate_word(word_file, log_file):
    log = open(log_file,"w")
    word = open(word_file,"r")
    word_content = word.readlines()

    first_header = word_content[0].replace("\n","")
    second_header = word_content[1].replace("\n","")
    if first_header == "" or second_header != "":
        print("Error: words file read. The words file header is incorrectly formatted",file=log)
        sys.exit()

    i = 2
    while i < len(word_content):
        the_word = word_content[i].strip()
        if the_word.replace(" ","") == "":
            print(f"Error: words file read. The banned word is invalid on line {i+1}",file=log)
            sys.exit()
        i += 1
    
    word.close()
    log.close()



def censor_forum(word_file, forum_file):
    word = open(word_file,"r")
    word_content = word.readlines()
    forum = open(forum_file,"r")
    forum_content = forum.readlines()
    new_forum = forum_content[:]

    i = 2
    while i < len(word_content):
        banned_word = word_content[i].lower().strip()
        after_banned = "*" * len(banned_word)

        j = 4
        while j < len(forum_content):
            info_forum = " " + new_forum[j] + " "
            single_word = info_forum.lower().split(banned_word) # split the forum information by banned words

            if len(single_word)>1:
                k = 1
                new_line = ""
                # check if it is a "real" banned word
                while k < len(single_word):
                    before_word = single_word[k-1][-1].isalpha() or single_word[k-1][-1]=="-" or single_word[k-1][-1]=="/"
                    after_word = single_word[k][0].isalpha() or single_word[k][0]=="-" or single_word[k][0]=="/"
                    not_banned = before_word or after_word
                    if not not_banned:
                        new_line = new_line + single_word[k-1] + after_banned
                    else:
                        new_line = new_line + single_word[-1] + banned_word
                    k += 1
                if not not_banned:
                    new_forum[j] = new_line + single_word[-1]
                    new_forum[j] = new_forum[j][1:-1]
            j += 3
        i += 1
    
    # return to the upperclass letters if needed
    k = 0
    while k < len(new_forum):
        new_line = list(new_forum[k])
        old_line = list(forum_content[k])
        j = 0
        while j < len(new_line):
            if new_line[j] != old_line[j]:
                if new_line[j].isalpha():
                    new_line[j] = old_line[j]
                    new_forum[k] = ''.join(new_line)
            j += 1
        k += 1

    forum.close()
    forum = open(forum_file,"w")
    forum.writelines(new_forum)
    forum.close()
    word.close()



class User:
    def __init__(self, name):
        self.name = name
        self.engagement = 0.0
        self.expressiveness = 0.0
        self.offensiveness = 0.0

    def calculate_personality_score(self):
        score = self.expressiveness - self.offensiveness
        if score > self.engagement:
            score = self.engagement
        return int(score)

    def process_message(self, message, banned_word):
        if isinstance(message, str) == False:
            return False
        
        if message[0] == "\t":
            times = 1.0
        else:
            times = 1.5
        
        self.engagement += 1*times
        
        exclamation = False
        question = False
        
        i = 0
        while i < len(message):
            if message[i] == "!":
                exclamation = True
            if message[i] == "?":
                question = True
            i += 1
        
        if exclamation:
            if question:
                self.expressiveness += 2*times
            else:
                self.expressiveness += 1*times
        else:
            if not question:
                self.expressiveness -= 1*times
        
        is_banned = False
        j = 0

        while j < len(banned_word):
            message = " " + message + " "
            single_word = message.split(banned_word[j])
            if len(single_word) > 1:
                k = 1
                while k < len(single_word):
                    before_word = single_word[k-1][-1].isalpha() or single_word[k-1][-1]=="-" or single_word[k-1][-1]=="/"
                    after_word = single_word[k][0].isalpha() or single_word[k][0]=="-" or single_word[k][0]=="/"
                    not_banned = before_word or after_word
                    if not not_banned:
                        is_banned = True
                    k += 1
            j+=1

        if is_banned:
            self.offensiveness += 1*times
        return True



def evaluate_forum(people_file, forum_file, word_file):
    people = open(people_file,"r")
    forum = open(forum_file,"r")
    word = open(word_file,"r")
    people_content = people.readlines()
    forum_content = forum.readlines()
    word_content = word.readlines()

    banned_word = []
    i = 2
    while i < len(word_content):
        banned_word.append(word_content[i].lower().strip())
        i += 1

    new_people = []
    new_people.append(people_content[0])
    new_people.append(people_content[1])
    
    # calculate the new score for every person
    s = 2
    while s < len(people_content):
        old_name, old_score = people_content[s].split(",")
        old_score = old_score.strip()
        the_user = User(old_name)

        j = 4
        while j < len(forum_content):
            single_name = forum_content[j-1].strip().replace("\t","")
            
            message = forum_content[j].lower().strip("\n")
            if single_name == old_name:
                the_user.process_message(message, banned_word)            
            j += 3
        
        the_score = the_user.calculate_personality_score()
        people_score = int(old_score) + the_score
        if people_score > 10:
            people_score = 10
        if people_score < -10:
            people_score = -10

        new_content = old_name + "," + str(people_score) + "\n"
        new_people.append(new_content)
        s += 1

    # make the people in descending order by personality score
    h = 2
    new_file = []
    while h < len(new_people):
        name, score = new_people[h].split(",")
        score = score.strip()
        new_file.append([int(score), len(new_people)-h, name])
        h += 1

    new_file.sort(reverse = True)

    m = 0
    write_file = people_content[0] + people_content[1]
    while m < len(new_file):
        new_scores = new_file[m]
        write_file = write_file + f"{new_scores[2]},{new_scores[0]}\n"
        m += 1

    word.close()
    forum.close()
    people.close()
    people = open(people_file,"w")
    people.write(write_file)
    people.close()



def main():
    command_line = [""] * 5
    i = 0
    while i < len(sys.argv):
        current_argv = sys.argv[i]
        if current_argv == "-task":
            command_line[0] = sys.argv[i+1]
        if current_argv == "-log":
            command_line[1] = sys.argv[i+1]
        if current_argv == "-forum":
            command_line[2] = sys.argv[i+1]
        if current_argv == "-words":
            command_line[3] = sys.argv[i+1]
        if current_argv == "-people":
            command_line[4] = sys.argv[i+1]
        i += 1
    
    command_arg = ["task","log","forum","words","people"]
    j = 0
    task_list = ["rank_people","validate_forum","censor_forum","evaluate_forum"]

    # check if an argument is not provided
    while j < len(command_line):
        if command_line[j] == "":
            print(f"No {command_arg[j]} arguments provided.")
            sys.exit()
        j += 1

    # check if the task argument match a value in the options list
    k = 0
    valid_task = False
    while k < len(task_list):
        if task_list[k] == command_line[0]:
            valid_task = True
        k += 1
    if valid_task == False:
        print("Task argument is invalid.")
        sys.exit()
    
    #check if all file can be read
    l = 2
    file_list = []
    while l < len(command_line):
        try:
            the_file = open(command_line[l])
            file_list.append(the_file)
        except FileNotFoundError:
            print(f"{command_line[l]} cannot be read.")
            sys.exit()
        l += 1

    print("Moderator program starting...")
    
    if command_line[0] == "rank_people":
        rank_people(command_line[4], command_line[1])
        sys.exit()
    elif command_line[0] == "validate_forum":
        validate_forum(command_line[2], command_line[1])
        sys.exit()
    elif command_line[0] == "censor_forum":
        validate_word(command_line[3], command_line[1])
        validate_forum(command_line[2], command_line[1])
        censor_forum(command_line[3], command_line[2])
        sys.exit()
    elif command_line[0] == "evaluate_forum":
        validate_forum(command_line[2], command_line[1])
        validate_word(command_line[3], command_line[1])
        rank_people(command_line[4], command_line[1])
        evaluate_forum(command_line[4], command_line[2], command_line[3])
        sys.exit()



if __name__ == "__main__":
    main()

