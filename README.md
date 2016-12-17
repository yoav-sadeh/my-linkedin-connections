# The LinkedIn Connection

A High level selenium based LinkedIn scraping DSL

**Purpose**

Selenium is a powerful framework that enables us to manipulate our browser in user like manner.

However, selenium&#39;s DSL is quite low level and due to its generic nature, it does not pretend to protect the developer from erroneous use: for example, one might think it would be a good idea to cache web elements and reuse them later(at any time). Of course, this could be dangerous since from the moment that the DOM changes in that element&#39;s area(should it be a page refresh, node deletion/manipulation etc.), the element is useless and any method invokation of that element would cause an exception.

The purpose of this project is to offer(given the site&#39;s specific behavior) a pattern that:

1. Eliminates selenium&#39;s verbosity(brings us back to pythonic minimal and simple code).
2. Provides easy access to the site&#39;s business entities.
3. Enables the developer to leverages Python&#39;s collections and iterators
4. And that&#39;s only the start :)

**Use Example:**

```
from linkedin_model import LinkedInPage, EntityType

def con_filter(emp):
   return emp.shared_connections != None and len(emp.shared_connections) > 0

linked_in = LinkedInPage('<mail_address>', '<pwd>') #todo: transfer to config
try:
   search_results_page = linked_in.search(EntityType.Companies, '<company_to_search>')
   company_iterator = search_results_page.get_entities_iterator(lambda x: x.name.lower() == '<company_to_search>')
   refined_search = [ent for ent in company_iterator if ent.web_site == '<company_web_site>']

   for bee in refined_search:
       bee_eye_page = search_results_page.go_to_result_page(bee)
       bee_eye_employees_page = bee_eye_page.go_to_employees_page()

       employees_with_connections = filter(con_filter,  bee_eye_employees_page.entities_previews)
       for emp in employees_with_connections:
           print '{}: {}'.format(emp.name, emp.shared_connections)
finally:
   linked_in.close()
```

**Disclaimer:**

This project is not by any meana production ready and is only a POC/proposition.