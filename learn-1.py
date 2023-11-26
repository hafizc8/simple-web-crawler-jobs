import requests
from bs4 import BeautifulSoup
from rich.progress import Progress
from rich.table import Table
from rich.console import Console

console = Console()

# request main page
main_page = requests.get("https://realpython.github.io/fake-jobs/")
# parse with bs
soup = BeautifulSoup(main_page.content, "html.parser")
# get jobs card
job_elements = soup.find(id="ResultsContainer").find_all("div", class_="card-content")

with Progress() as progress:
    # start progress in console
    task1 = progress.add_task("[green bold]Processing...", total=15)
    num_of_completed = 0
    jobs_data = []

    # looping each jobs card
    for job_element in job_elements:

        if (num_of_completed != 15):
            # get text of element we need
            job_title = job_element.find("h2", class_="title").text.strip()
            company = job_element.find("h3", class_="subtitle").text.strip()
            location = job_element.find("p", class_="location").text.strip()
            link_detail = job_element.find("a", string="Apply")['href'].strip()

            # request detail page for getting attributes: description, and posted date
            detail_page = requests.get(link_detail)

            if (detail_page.status_code == 200) :
                # parse with bs
                soup_detail = BeautifulSoup(detail_page.content, "html.parser")

                # get text of element in detail page
                content_wrapper = soup_detail.find("div", class_="content")
                description = content_wrapper.find("p").text.strip()
                date_posted = content_wrapper.find("p", id="date").text.strip().split(" ")[1]

                # append/collect data to list
                jobs_data.append({'job_title': job_title, 'company': company, 'location': location, 'description': description, 'date_posted': date_posted})
                
                # update progress
                num_of_completed = num_of_completed + 1
                progress.update(task1, advance=1, description=f"[yellow]Scrapping {num_of_completed} of {15} items ..")

# print result in console
table = Table(show_header=True, header_style="bold magenta", title=f"Result Table", title_style="bold magenta")
table.add_column("Job Title", width=35)
table.add_column("Company", width=10)
table.add_column("Location", width=20)
table.add_column("Description", width=20)
table.add_column("Date Posted", width=20)

for job in jobs_data:
    table.add_row(job['job_title'], job['company'], job['location'], job['description'], job['date_posted'], style='magenta')

console.print(table)