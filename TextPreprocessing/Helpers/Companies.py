import Config.text


def replace_companies(text):
    COMPANIES = {
        "Apple": " " + Config.text.company + " ",
        "Biohit": " " + Config.text.company + " ",
        "Componenta": " " + Config.text.company + " ",
        "Facebook": " " + Config.text.company + " ",
        "Finnish Aktia Group": " " + Config.text.company + " ",
        "Finnish Bank of +àland": " " + Config.text.company + " ",
        "Finnlines": " " + Config.text.company + " ",
        "Fiskars": " " + Config.text.company + " ",
        "Google": " " + Config.text.company + " ",
        "HELSINKI ( AFX )": " " + Config.text.company + " ",
        "HKScan": " " + Config.text.company + " ",
        "Kemira": " " + Config.text.company + " ",
        "MegaFon": " " + Config.text.company + " ",
        "Metso Minerals": " " + Config.text.company + " ",
        "Microsoft": " " + Config.text.company + " ",
        "Nokia Corp.": " " + Config.text.company + " ",
        "Nordea Group": " " + Config.text.company + " ",
        "Ponsse": " " + Config.text.company + " ",
        "Ramirent": " " + Config.text.company + " ",
        "Ruukki": " " + Config.text.company + " ",
        "Sanoma Oyj HEL": " " + Config.text.company + " ",
        "Talentum": " " + Config.text.company + " ",
        "Teleste Oyj HEL": " " + Config.text.company + " ",
        "TeliaSonera TLSN": " " + Config.text.company + " ",
        "Tesla": " " + Config.text.company + " ",
        "Tiimari": " " + Config.text.company + " ",
        "Vaahto Group": " " + Config.text.company + " ",
    }
    text = text.split()
    reformed = [COMPANIES[word] if word in COMPANIES else word for word in text]
    return " ".join(reformed)
