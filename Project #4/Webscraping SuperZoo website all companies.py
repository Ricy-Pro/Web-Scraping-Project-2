from bs4 import BeautifulSoup
import requests
import csv

url = "https://s23.a2zinc.net/clients/WPA/SZ2022/Public/Exhibitors.aspx?Index=All"

try:
    result = requests.get(url)
    result.raise_for_status()  # Check for HTTP request errors
    soup = BeautifulSoup(result.text, "html.parser")
    titlu= soup.title
    product_elements = soup.find_all("tr")
    a = 0
    company_details = []
    def get_info(url1):
     try:
        results1 = requests.get(url1)
        results1.raise_for_status()  
        soup1 = BeautifulSoup(results1.text, "html.parser")
        find_description = soup1.find("div", {"id": "eboothContainer"})
        name1 = soup1.find("h1").text.strip()
        city1 = soup1.find("span", {"class": "BoothContactCity"}).text.strip()
        country1 = soup1.find("span", {"class": "BoothContactCountry"}).text.strip()
        website_link1 = soup1.find("span", {"class": "BoothContactUrl"}).text.strip()
        linkedin1 = soup1.find("a", {"id": "ctl00_ContentPlaceHolder1_ctrlCustomField_Logos_dlCustomFieldList_ctl01_lnkCustomField"})['href'] if soup1.find("a", {"id": "ctl00_ContentPlaceHolder1_ctrlCustomField_Logos_dlCustomFieldList_ctl01_lnkCustomField"}) else "-"
        brands1 = soup1.find("p", {"class": "BoothBrands"}).text.strip() if soup1.find("p", {"class": "BoothBrands"}) else "-"
        state1 = soup1.find("span", {"class": "BoothContactState"}).text.strip() if soup1.find("span", {"class": "BoothContactState"}) else "-"
        description_tag = find_description.find_all("p")
        description1 = " ".join([description.text.strip() for description in description_tag if description.text.strip() != "" and description.text.strip() != brands1])
        
        company_details.append({
            "Name": name1,
            
            "Country": country1,
            "City": city1,
            "State": state1,
            "Website_link": website_link1,
            "Brands": brands1,
            "Description": description1,
            "LinkedIn Url":linkedin1
        })

     except Exception as e:
        print(f"An error occurred while extracting data from {url1}: {e}")

   
        
        
        
        
        
    for product in product_elements[3:-1]:
            link = product.find("a", {"class": "exhibitorName"})['href']
            complete_link = "https://s23.a2zinc.net/clients/WPA/SZ2022/Public/" + link
            get_info(complete_link)
            

    csv_filename = "Pet Industry Companies from the SuperZoo Aug 2023 Conference Website.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "Country", "City","State","Website_link","Brands","Description","LinkedIn Url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(company_details)

    print(f"Scraped data saved to {csv_filename}")

except requests.exceptions.RequestException as req_exc:
    print(f"An error occurred during the HTTP request: {req_exc}")
except Exception as e:
    print(f"An error occurred: {e}")
