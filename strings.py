import mysql.connector
import os
import discord.message
from dotenv import load_dotenv

load_dotenv()
DATABASE_PASSWORD = os.environ.get('DB_PASS')
langs = {}
def use_database(command, fetch=False, commit=False):
    _ = None
    conn = mysql.connector.connect(
    host='freedb.tech',
    user='freedbtech_Nikicoraz',
    password=DATABASE_PASSWORD,
    database='freedbtech_generale')
    c = conn.cursor()
    c.execute(command)
    if fetch:
        _ = c.fetchall()
    if commit:
        conn.commit()
    conn.close()
    return _

def reload_lang():
    for ch, la in use_database('SELECT * FROM lang', fetch=True):
        langs[ch] = la
reload_lang()

def get_string(ctx : discord.Message, string_):
    if langs.get(ctx.guild.id) == 'it' or langs.get(ctx.guild.id, None) == None:
        return STRINGS.get(string_, 'ERRORE DI TRADUZIONE')[0]
    elif langs.get(ctx.guild.id) == 'en':
        return STRINGS.get(string_, 'TRANSLATION ERROR')[1]




STRINGS = {
    'no_ling':('Lingua non riconosciuta', 'Language not recognized'),
    'probabilita':(' ha una probabilità del ', ' has a probability of '),
    'admin_error':('Solo un admin può usare questo comando! ', 'Only an admin user can use this command! '),
    'creator_error':('Solo il creatore di questo bot può usare questo comando! ', 'Only the bot creator can use this command! '),
    'warn':(' è stato avvertito per ', ' has been warned for '),
    'infrazione':('infrazione', 'infraction'),
    'in_data':('in data', 'on'),
    'mai_infra':("non ha mai fatto un'infrazione", 'has never made an infraction'),
    'fed_pen_di':('Fedina penale di', 'Criminal record of'),
    'pulita_con_succ':('pulita con successo!', 'cleaned with success!'),
    'kick_error':('Non hai i permessi per kiccare le persone!', 'You don\'t have permission to kick people!'),
    'kick_amm':('Non si può kiccare l\'amministratore! :(', 'You can\'t kick an administrator :('),
    'ban_error':('Non hai i permessi per bannare le persone!', 'You don\'t have permission to ban people!'),
    'ban_amm':('Non si può bannare l\'amministratore! :(', 'You can\'t ban an administrator :('),
    'canc_errore':('Non puoi cancellare più di 5000 messaggi!!!', 'You can\'t delete more than 5000 messages!!!'),
    'costo':('Messaggi cancellati, ora pagami', 'Messeges deleted, now pay me'),
    'dado':('Lanciando il dado...', 'Rolling the dice...'),
    'testa':('testa', 'head'),
    'croce':('croce', 'tails'),
    'uscito':('è uscito ', ''),
    'motivante':('Eccoti una immagine motivante :wink:', 'Here\'s a motivating image :wink:'),
    'scaricalo':('Scaricalo!', 'Download it!'),
    'gia_silenziato':('è già stato silenziato!', 'has already been silenced!'),
    'silenziato': ('è stato silenziato', 'has been silenced'),
    'no_silenziato':('non è stato silenziato!', 'hasn\'t been silenced!'),
    'ricordato_parlare':('si è ricordato come parlare!', 'has remembered how to talk!'),
    'no_scelta':('Quando non hai scelta', 'When you have no choice'),
    'help':('ciao, usa $help <comando> per avere piu\' informazioni!', 'hello, use the $help <command> to have more information!'),
    'creatore':('creatore', 'creator'),
    'v_casual':('''aggiungi_insulto(ai), mostra_infrazioni(mi), insulta(i),
         probabilita(p), dado, tris, coin, gaymeter(gm), emoji_animate, ispira,
         crediti, morracinese(mc), choose, impersona''', '''show_infractions(mi), probability(p), dice, tris, coin, animated_emojis, inspire,
         credits, choose, impersonate'''),
    'immagini':('Immagini', 'Images'),
    'v_immagini':('avatar, grigio, linee, buff, pirata, brucia', 'avatar, gray, lines, buff, pirate, burn'),
    'matematica':('Matematica', 'Math'),
    'v_matematica':('somma, dividi, moltiplica', 'sum, divide, multiply'),
    'warn_d':('Aggiunge una infrazione sulla fedina di una persona', 'Adds an infraction on a criminal record of a person'),
    'sintassi':('**Sintassi**', '**Syntax**'),
    'warn_v':('$warn <persona> [ragione]', '$warn <person> [motive]'),
    'mostr_infr':('Mostra Infrazioni', 'Show Infractions'),
    'd_mostr_infr':('Mostra le infrazioni penali di una persona', 'Show the infractions of a person'),
    'v_mostr_infr':('$mostra_infrazioni <persona>', '$show_infractions <person>'),
    'prob':('Probabilita', 'Probability'),
    'd_prob':('Probabilità che succeda una cosa', 'Probability that something happens'),
    'v_prob':('$probabilita [cosa che deve accadere]', '$probability [thing]'),
    'd_kick':('Caccia una persona dal server', 'Kicks a person from the server'),
    'v_kick':('$kick <persona> [motivo]', '$kick <person> [motive]'),
    'd_ban':('Banna una persona dal server', 'Bans a person from the server'),
    'v_ban':('$ban <persona> [motivo]', '$ban <person> [motive]'),
    'nessuno':('Nessuno', 'None'),
    'd_clean':('Pulisce la chat', 'Cleans the chat'),
    'v_clean':('$clean {persona o numero di messaggi}', '$clean {person or number of messages}'),
    'dado_n':('dado', 'dice'),
    'd_dado':('Lancia un dado e sceglie un numero tra 1 e 6', 'Rolls a dice and chooses a number between 1 and 6'),
    'v_dado':('$dado', '$dice'),
    'd_tris':('Comincia una partita a tris', 'Begin a tris match'),
    'v_tris':('$tris <persona>', '$tris <person>'),
    'd_coin':('Lancia una monetina', 'Throw a coin'),
    'em_an':('Emoji Animate', 'Animated Emojis'),
    'd_em_an':('Lista della emoji animate', 'Animated emoji list'),
    'grigio':('grigio','gray'),
    'd_grigio':('Visualizza una immagine profilo in una scala di grigi', 'View a profile image in grayscale'),
    'v_grigio':('$grigio <persona>', '$gray <person>'),
    'd_buff':('Fatti diventare un figo muscoloso', 'Become a cool buff guy'),
    'v_buff':('$buff <persona>', '$buff <person>'),
    'v_pirate':('$pirata <persona>', '$pirate <person>'),
    'd_linee':('Visualizza le linee di una immagine profilo', 'Show the lines of a profile image'),
    'v_linee':('$linee <persona>', '$lines <person>'),
    'ispira':('ispira', 'inspire'),
    'd_ispira':('Manda una immagine motivante dal sito https://inspirobot.me', 'Send a motivational image from the site https://inspirobot.me'),
    'v_ispira':('$ispira', '$ispire'),
    'crediti':('Crediti', 'Credits'),
    'd_credits':('Creato da Nikicoraz\n[Github](https://github.com/Nikicoraz/gino)', 'Created by Nikicoraz\n[Github](https://github.com/Nikicoraz/gino)'),
    'd_avatar':('Scarica l\'avatar di una persona nel server!', 'Download the avatar of a person!'),
    'v_avatar':('$avatar <persona>', '$avatar <person>'),
    'brucia':('brucia', 'burn'),
    'd_brucia':('Brucia una persona', 'Burn someone'),
    'v_brucia':('$brucia <persona>', '$burn <person>'),
    'd_mute':('Togli il diritto di parola ad una persona', 'Remove freedom of speech'),
    'v_mute':('$mute <persona>', '$mute <person>'),
    'd_unmute':('Ridai tristemente il diritto di parola ad una persona', 'Since the riots have gotten stronger, you sadly have to give back freedom of speech'),
    'v_unmute':('$unmute <persona>', '$unmute <person>'),
    'd_choose':('Scegli tra alcune opzioni', 'Choose between options'),
    'v_choose':('$choose [opzioni separate da ","]', '$choose [options separated by ","]'),
    'impersona':('impersona', 'Impersonate'),
    'd_impersona':('Fai finta di essere qualcun altro', 'Be someone else!'),
    'v_impersona':('$impersona <persona> [messaggio]', '$impersonate <person> [message]'),
    'pareggio':('Pareggio!', 'Draw!'),
    'vincitore_e':("Il vincitore è ", 'The winner is '),
    'partita_in_corso':('Una partita è già in corso!', 'There\'s already a game ongoing!'),
    'solo':('Non pensavo fossi così triste', 'I didn\'t know you were this lonely'),
    'gioco_con_bot':('Vuoi giocare con un bot? :thinking:', 'Do you want to play with a bot? :thinking:'),
    'sfida':('accetti la sfida?', 'accept the challenge?'),
    'timeout':('non ha risposto in tempo', 'didn\'t answer in time'),
    'accept':('ha accettato la sfida!', 'accepted the challenge!'),
    'decline':('è un codardo e ha rifiutato la sfida!', 'is a coward and declined the challenge!'),
    'reg_tris':('Inserisci un numero da 1 a 9 per posizionare', 'Insert a number from 1 to 9 to position on the game board'),
    'timeout60':('Nessuna risposta da 60 secondi, mi ignorate :cry:? Addio', 'No response in 60 seconds, are you ignoring me :cry:? Goodbye'),
    'turno_di':('Attualmente è il turno di ', 'It\'s the turn of '),
    'number_19':('Inserisci un numero tra 1 e 9!', 'Insert a number between 1 and 9!'),
    'occupato':("Casella già occupata!", 'This place is already occupied!'),
    'da_solo':("Vuoi giocare da solo? :thinking:", 'Do you want to play alone? :thinking:'),
    'immaginary':("Non conosco il tuo amico immaginario :neutral_face:", 'I don\'t know your immaginary friend :neutral_face:')


    }