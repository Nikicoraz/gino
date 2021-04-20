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
    'v_matematica':('somma, dividi, moltiplica', 'sum, divide, multiply')
    
    }