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
    elif langs.get(ctx.guild.id) == 'OwO':
        return STRINGS.get(string_, 'TRWANSLATWION EWRROR o.O')[2]




STRINGS = {
    'no_ling':('Lingua non riconosciuta', 'Language not recognized','Langwuage nwot recognwized'),
    'probabilita':(' ha una probabilità del ', ' has a probability of ', ' hwas a prowbabwility owf '),
    'admin_error':('Solo un admin può usare questo comando! ', 'Only an admin user can use this command! ', 'Owly an awdmin uwser can uwse twis cowmmand! '),
    'creator_error':('Solo il creatore di questo bot può usare questo comando! ', 'Only the bot creator can use this command! ', 'Ownly twhe bwot creatwor can uwse twis cowmmand! '),
    'warn':(' è stato avvertito per ', ' has been warned for ', ' has bween warnwed fwor '),
    'infrazione':('infrazione', 'infraction', 'inwfracwtion'),
    'in_data':('in data', 'on', 'on'),
    'mai_infra':("non ha mai fatto un'infrazione", 'has never made an infraction', 'has newver mawde awn infrwaction'),
    'fed_pen_di':('Fedina penale di', 'Criminal record of', 'ÒwÓ Criwminal rewcord of'),
    'pulita_con_succ':('pulita con successo!', 'cleaned with success!', 'cwleaned with suwccess!'),
    'kick_error':('Non hai i permessi per kiccare le persone!', 'You don\'t have permission to kick people!', 'You dwon\'t have pewrmission to kick pweople!'),
    'kick_amm':('Non si può kiccare l\'amministratore! :(', 'You can\'t kick an administrator :(', 'You cwan\'t kwick an admwinistrator ÒwÓ'),
    'ban_error':('Non hai i permessi per bannare le persone!', 'You don\'t have permission to ban people!', 'You dwon\'t have permwission to bwan pweople!'),
    'ban_amm':('Non si può bannare l\'amministratore! :(', 'You can\'t ban an administrator :(', 'You cwan\'t bwan an adwministrator ÒwÓ'),
    'canc_errore':('Non puoi cancellare più di 5000 messaggi!!!', 'You can\'t delete more than 5000 messages!!!', 'You cwan\'t dwelete more twan 5000 mewssages OwO'),
    'costo':('Messaggi cancellati, ora pagami', 'Messages deleted, now pay me', 'Mewssages dweleted, now pway me UwU'),
    'dado':('Lanciando il dado...', 'Rolling the dice...', 'Rowlling the dice...'),
    'testa':('testa', 'head','hwead'),
    'croce':('croce', 'tails','twails'),
    'uscito':('è uscito ', 'It exit ','It ewxit '),
    'motivante':('Eccoti una immagine motivante :wink:', 'Here\'s a motivating image :wink:'),
    'scaricalo':('Scaricalo!', 'Download it!', 'Download it !!'),
    'gia_silenziato':('è già stato silenziato!', 'has already been silenced!', 'has awlready bween silwenced!'),
    'silenziato': ('è stato silenziato', 'has been silenced', 'has bween silwenced'),
    'no_silenziato':('non è stato silenziato!', 'hasn\'t been silenced!', 'hawsn\'t bween silwenced!'),
    'ricordato_parlare':('si è ricordato come parlare!', 'has remembered how to talk!', 'has rewmembered how to twalk!'),
    'no_scelta':('Quando non hai scelta', 'When you have no choice', 'When you hwave nwo chwoice'),
    'help':('ciao, usa $help <comando> per avere piu\' informazioni!', 'hello, use the $help <command> to have more information!', 'hewllo, use the $help <command> to hwave mwore infowrmation!'),
    'creatore':('creatore', 'creator', 'cwreator'),
    'v_casual':('''aggiungi_insulto(ai), mostra_infrazioni(mi), insulta(i),
         probabilita(p), dado, tris, coin, gaymeter(gm), emoji_animate, ispira,
         crediti, morracinese(mc), choose, impersona, furrymeter''', '''show_infractions(mi), probability(p), dice, tris, coin, animated_emojis, inspire,
         credits, choose, impersonate, furrymeter''', '''show_inwfractions(mi), prowbability(p), dwice, twris, cowin, anwimated_emowjis, inwspire,
         credits, chwoose, imwpersonate, fuwrrymeter'''),
    'immagini':('Immagini', 'Images', 'Iwmages'),
    'v_immagini':('avatar, grigio, linee, buff, pirata, brucia', 'avatar, gray, lines, buff, pirate, burn', 'awvatar, gwray, lwines, bwuff, pwirate, bwurn'),
    'matematica':('Matematica', 'Math', 'Mwath'),
    'v_matematica':('somma, dividi, moltiplica', 'sum, divide, multiply', 'swum, dwivide, mwultiply'),
    'warn_d':('Aggiunge una infrazione sulla fedina di una persona', 'Adds an infraction on a criminal record of a person', 'Awdds an iwnfraction on a cwriminal rwecord of a pwerson ÒwÓ'),
    'sintassi':('**Sintassi**', '**Syntax**', '**Swyntax**'),
    'warn_v':('$warn <persona> [ragione]', '$warn <person> [motive]', '$warn <pwerson> [mwotive]'),
    'mostr_infr':('Mostra Infrazioni', 'Show Infractions', 'Swhow Inwfractions'),
    'd_mostr_infr':('Mostra le infrazioni penali di una persona', 'Show the infractions of a person', 'Swhow twhe iwnfractions of a pwerson'),
    'v_mostr_infr':('$mostra_infrazioni <persona>', '$show_infractions <person>', '$swhow_iwnfractions <pwerson>'),
    'prob':('Probabilita', 'Probability', 'Pwrobability'),
    'd_prob':('Probabilità che succeda una cosa', 'Probability that something happens', 'Pwrobability twhat somewthing hawppens'),
    'v_prob':('$probabilita [cosa che deve accadere]', '$probability [thing]', '$pwrobability [twhing]'),
    'd_kick':('Caccia una persona dal server', 'Kicks a person from the server','Kwicks a pwerson fwrom twhe swerver'),
    'v_kick':('$kick <persona> [motivo]', '$kick <person> [motive]', '$kwick <pwerson> [mwotive]'),
    'd_ban':('Banna una persona dal server', 'Bans a person from the server', 'Bwans a pwerson from twhe swerver'),
    'v_ban':('$ban <persona> [motivo]', '$ban <person> [motive]', '$bwan <pwerson> [mwotive]'),
    'nessuno':('Nessuno', 'None', 'Nwone'),
    'd_clean':('Pulisce la chat', 'Cleans the chat', 'Cwleans twhe cwhat'),
    'v_clean':('$clean {persona o numero di messaggi}', '$clean {person or number of messages}', '$cwlean {pwerson or nwumber of mwessages}'),
    'dado_n':('dado', 'dice','Dwice'),
    'd_dado':('Lancia un dado e sceglie un numero tra 1 e 6', 'Rolls a dice and chooses a number between 1 and 6','Rwolls a dwice and cwhooses a nwumber bwetween 1 awnd 6'),
    'v_dado':('$dado', '$dice', '$dwice'),
    'd_tris':('Comincia una partita a tris', 'Begin a tris match', 'Bwegin a twris mwatch'),
    'v_tris':('$tris <persona>', '$tris <person>', '$twris <pwerson>'),
    'd_coin':('Lancia una monetina', 'Throw a coin', 'Twhrow a cwoin'),
    'em_an':('Emoji Animate', 'Animated Emojis', 'Awnimated Ewmojis'),
    'd_em_an':('Lista della emoji animate', 'Animated emoji list', 'Awnimated ewmoji lwist'),
    'grigio':('grigio','gray','gwray'),
    'd_grigio':('Visualizza una immagine profilo in una scala di grigi', 'View a profile image in grayscale', 'Vwiew a pwrofile iwmage in gwrayscale'),
    'v_grigio':('$grigio <persona>', '$gray <person>', '$gwray <pwerson>'),
    'd_buff':('Fatti diventare un figo muscoloso', 'Become a cool buff guy', 'Bwecome a cwool bwuff pwerson'),
    'v_buff':('$buff <persona>', '$buff <person>','$bwuff <pwerson>'),
    'v_pirate':('$pirata <persona>', '$pirate <person>', '$pwirate <pwerson>'),
    'd_linee':('Visualizza le linee di una immagine profilo', 'Show the lines of a profile image', 'Swhow twhe lwines of a pwrofile iwmage'),
    'v_linee':('$linee <persona>', '$lines <person>', '$lwines <pwerson>'),
    'ispira':('ispira', 'inspire', 'iwnspire'),
    'd_ispira':('Manda una immagine motivante dal sito https://inspirobot.me', 'Send a motivational image from the site https://inspirobot.me', 'Swend a mwotivational iwmage fwrom twhe swite https://inspirobot.me'),
    'v_ispira':('$ispira', '$ispire', '$iwspire'),
    'crediti':('Crediti', 'Credits', 'Cwredits'),
    'd_credits':('Creato da Nikicoraz\n[Github](https://github.com/Nikicoraz/gino) \n Tradotto a OwO da [Federico](https://www.youtube.com/channel/UC4tQZ5B0Pe4LN476NfTu0Cw)', 'Created by Nikicoraz\n[Github](https://github.com/Nikicoraz/gino) \n Transalted to OwO by [TheCat](https://www.youtube.com/channel/UC4tQZ5B0Pe4LN476NfTu0Cw)', 'Cwreated by Nwikicoraz\n[Github](https://github.com/Nikicoraz/gino) \n Twranslated to OwO by [TwheCat](https://www.youtube.com/channel/UC4tQZ5B0Pe4LN476NfTu0Cw)'),
    'd_avatar':('Scarica l\'avatar di una persona nel server!', 'Download the avatar of a person!', 'Dwownload twhe awvatar of a pwerson!'),
    'v_avatar':('$avatar <persona>', '$avatar <person>' , '$awvatar <pwerson>'),
    'brucia':('brucia', 'burn', 'bwurn'),
    'd_brucia':('Brucia una persona', 'Burn someone', 'Bwurn swomeone'),
    'v_brucia':('$brucia <persona>', '$burn <person>', '$bwurn <pwerson>'),
    'd_mute':('Togli il diritto di parola ad una persona', 'Remove freedom of speech', 'Rwemove fwreedom of swpeech'),
    'v_mute':('$mute <persona>', '$mute <person>', '$mute <pwerson>'),
    'd_unmute':('Ridai tristemente il diritto di parola ad una persona', 'Since the riots have gotten stronger, you sadly have to give back freedom of speech', 'Swince the rwiots have gwotten strwonger, you swadly ;-; have to gwive bwack fwreedom of swpeech'),
    'v_unmute':('$unmute <persona>', '$unmute <person>', '$unmute <pwerson>'),
    'd_choose':('Scegli tra alcune opzioni', 'Choose between options', 'Cwhoose bwetween owptions'),
    'v_choose':('$choose [opzioni separate da ","]', '$choose [options separated by ","]', '$cwhoose [owptions sweparated bwy ","'),
    'impersona':('impersona', 'Impersonate', 'Iwmpersonate'),
    'd_impersona':('Fai finta di essere qualcun altro', 'Be someone else!', 'Bwe swomeone ewlse!'),
    'v_impersona':('$impersona <persona> [messaggio]', '$impersonate <person> [message]', '$iwmpersonate <pwerson> [mwessage]'),
    'pareggio':('Pareggio!', 'Draw!', 'Drwaw'),
    'vincitore_e':("Il vincitore è ", 'The winner is ', 'Twhe winner is '),
    'partita_in_corso':('Una partita è già in corso!', 'There\'s already a game ongoing!', 'Twhere\'s awlready a gwame owngoing!'),
    'solo':('Non pensavo fossi così triste', 'I didn\'t know you were this lonely', 'I dwidn\'t kwnow you w-were this lwonely'),
    'gioco_con_bot':('Vuoi giocare con un bot? :thinking:', 'Do you want to play with a bot? :thinking:', 'Dwo you want to pwlay with a bwot? :thinking:'),
    'sfida':('accetti la sfida?', 'accept the challenge?', 'awccept the cwhallenge?'),
    'timeout':('non ha risposto in tempo', 'didn\'t answer in time','dwidn\'t awnswer in twime'),
    'accept':('ha accettato la sfida!', 'accepted the challenge!','awcepted the cwhallenge!'),
    'decline':('è un codardo e ha rifiutato la sfida!', 'is a coward and declined the challenge!','is a cwoward and dweclined the cwhallenge ÒwÓ!'),
    'reg_tris':('Inserisci un numero da 1 a 9 per posizionare', 'Insert a number from 1 to 9 to position on the game board', 'Iwnsert a nwumber fwrom 1 to 9 to pwosition on the gwame bwoard'),
    'timeout60':('Nessuna risposta da 60 secondi, mi ignorate :cry:? Addio', 'No response in 60 seconds, are you ignoring me :cry:? Goodbye', 'No rwesponse in 60 sweconds, are you i-iwgnoring me :cry:? Gwoodbye'),
    'turno_di':('Attualmente è il turno di ', 'It\'s the turn of ', 'It\'s the twurn of '),
    'number_19':('Inserisci un numero tra 1 e 9!', 'Insert a number between 1 and 9!', 'Iwnsert a nwumber bwetween 1 and 9!'),
    'occupato':("Casella già occupata!", 'This place is already occupied!', 'This pwlace is awlready owccupied!'),
    'da_solo':("Vuoi giocare da solo? :thinking:", 'Do you want to play alone? :thinking:','Do ywou want to pwlay awlone? ?-?'),
    'immaginary':("Non conosco il tuo amico immaginario :neutral_face:", 'I don\'t know your immaginary friend :neutral_face:', 'I dwon\'t kwnow your iwmmaginary fwriend :neutral_face:'),
    'gay':('è gay al', 'is gay at', 'is gway at'),
    'furry':('è furry al', 'is furry at', 'is fwurry at'),
    'd_gm':('Indica quanto è gay una persona', 'Show how much a person is gay', 'Show how mwuch a pwerson is gway OwO'),
    'v_gm':('$gaymeter <persona>', '$gaymeter <person>','$gaymeter <pwerson>'),
    'd_fm':('Indica quanto è furry una persona', 'Show how much a person is a furry', 'Show how mwuch a pwerson is a fwurry OwO'),
    'v_fm':('$furrymeter <persona>', '$furrymeter <person>', '$furrymeter <pwerson>')


    }