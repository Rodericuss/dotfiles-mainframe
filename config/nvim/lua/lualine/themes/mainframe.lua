local function mode(c) return {a={fg='#0D0C09',bg=c,gui='bold'},b={fg='#5BA89B',bg='#15130E'},c={fg='#CFC4AA',bg='#15130E'},z={fg='#0D0C09',bg='#B8925A'}} end
return {normal=mode('#9EEA8E'),insert=mode('#5BA89B'),visual=mode('#B8925A'),replace=mode('#D0553F'),command=mode('#C8743F'),inactive={a={fg='#6E5836',bg='#15130E'},b={fg='#6E5836',bg='#15130E'},c={fg='#6E5836',bg='#15130E'}}}
