url = "sdajklfnsdlfnsdfsdfsd-fasd-fq-rt4t4-fg-t-q34-t34-.pdf"
print(url.split("?", 1)[0].rpartition(".")[2])
# 1. Strip off any query string
base = url.split("?", 1)[0].rpartition(".")[2]
# 2. Partition at the last '.', then take the rightmost piece
after_last_dot = base.rpartition(".")[2]

print(after_last_dot)
