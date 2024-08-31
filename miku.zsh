clear

N=$(wc -l queue.txt | awk '{print $1}')
Np=$(sed 's/^const MIKUS = //' static/mikus.js | jq length)
Nc=$(sed 's/^const MIKUS = //' static/mikus.js | jq '[.[] | select(.coords == null)] | length')

figlet "miku.earth: $N" | lolcat -F 0.5

print -P "[3m%F{cyan italic}╰──────────  posted: $Np  ($Nc need coords)  queue: $(($N - $Np))  ────────────╯"
echo
cd $(dirname "$0")

PROMPT="[36m˶ᵔᵕᵔ˶[0m ↦ "

alias c="source miku.zsh"
alias f="python fetch.py"
alias p="python post_process.py"
alias qr="python miqueue.py > queue.txt; source miku.zsh"
alias q="less queue.txt"
alias qg="open https://www.tumblr.com/blog/miku-earth/queue"
qs() { grep -i $1 queue.txt; }