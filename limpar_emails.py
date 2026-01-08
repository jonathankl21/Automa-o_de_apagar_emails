import imaplib
import email
from email.header import decode_header
EMAIL_USER = "seu_email"
EMAIL_PASS = "sua_senha"  # A senha de 16 letras
IMAP_SERVER = "imap.gmail.com"
PALAVRAS_CHAVE = [""]


def conectar_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        return mail
    except Exception as e:
        print(f"Erro ao entrar: {e}")
        return None


def mover_para_lixeira(mail, email_id):
    pasta_destino = '[Gmail]/Lixeira'

    result = mail.copy(email_id, pasta_destino)

    if result[0] == 'OK':
        mail.store(email_id, '+FLAGS', '\\Deleted')
        print(f"E-mail {email_id.decode()} movido para a Lixeira.")
    else:
        print(f"Erro ao mover e-mail {email_id.decode()}. Motivo: {result}")




def main():
    mail = conectar_email()
    if not mail:
        return
    mail.select("INBOX")

    print("--- Começando a busca ---")

    for keyword in PALAVRAS_CHAVE:
        print(f"\n🔍 Buscando por: '{keyword}'...")
        status, messages = mail.search(None, f'(FROM "{keyword}")')
        email_ids = messages[0].split()[::-1]

        total = len(email_ids)
        print(f" Foram encontrados {total} e-mails.")

        if total > 0:
            for e_id in email_ids:
                res, msg_data = mail.fetch(e_id, '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
                raw_header = msg_data[0][1].decode('utf-8')
                print(f"Target: {raw_header.strip()}")

                mail.copy(e_id, '[Gmail]/Lixeira')
                mail.store(e_id, '+FLAGS', '\\Deleted')
                print(f"🗑️ Deletado ID {e_id.decode()}")
        try:
            mail.expunge()
            mail.close()
            mail.logout()
            print("\n--- Limpeza feita e conexão fechada ---")
        except:
            print("Gerou.")


if __name__ == "__main__":
    main()