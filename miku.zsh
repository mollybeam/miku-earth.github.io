clear

Nq=$(wc -l queue.txt | awk '{print $1}')
Nq2=$(wc -l queuetwo.tsv | awk '{print $1}')
N=$((Nq + Nq2))
Np=$(sed 's/^const MIKUS = //' static/mikus.js | jq length)
Nc=$(sed 's/^const MIKUS = //' static/mikus.js | jq '[.[] | select(.coords == null)] | length')
NC=$(sed 's/^const MIKUS = //' static/mikus.js | jq '[.[] | select(.country == null)] | length')

figlet "miku.earth: $N" | lolcat -F 0.5

print -P "[3m%F{cyan italic}╰────────────╮     posted: $Np  queue: $(($Nq - $Np))  queuetwo: $Nq2     ╭────────────╯"
print -P "[3m%F{red}             ╰───   $Nc need coords  $NC need country code   ───╯"


  
echo
cd $(dirname "$0")

PROMPT="[36m˶ᵔᵕᵔ˶[0m ↦ "

alias c="source miku.zsh"
alias f="python fetch.py"
alias p="python post_process.py"
alias g="open index.html"

alias q="less queue.txt"
alias qr="python miqueue.py > queue.txt; source miku.zsh"
alias qg="open https://www.tumblr.com/blog/miku-earth/queue"
qs() {
    grep -i $1 queue.txt;
    grep -i $1 queuetwo.tsv;
    }