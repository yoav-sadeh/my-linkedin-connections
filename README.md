# The LinkedIn Connection

A High level selenium based LinkedIn scraping DSL

**Purpose**

Selenium is a powerful framework that enables us to manipulate our browser in user like manner.

However, selenium&#39;s DSL is quite low level and due to its generic nature, it does not pretend to protect the developer from erroneous use: for example, one might think it would be a good idea to cache web elements and reuse them later(at any time). Of course, this could be dangerous since from the moment that the DOM changes in that element&#39;s area(should it be a page refresh, node deletion/manipulation etc.), the element is useless and any method invokation of that element would cause an exception.

The purpose of this project is to offer(given the site&#39;s specific behavior) a pattern that:

1. Eliminates selenium&#39;s verbosity(brings us back to pythonic minimal and expressive code).
2. Provides easy access to the site&#39;s business entities.
3. Enables the developer to leverage Python&#39;s collections and iterators
4. Uses Try monad(borrowed from haskell/scala) to better handle exceptions.
5. Provides a usefull skeleton to build any selenium based app(see page module).

**Road Map:**

1. Introduce locator module(already exists but not in use yet) to further separate business from selenium specifics and separate page operaions from specific locators.
2. Enable multiple aggregators within a single page(EntityPage/EntityAggregatorPage).
3. Provide a completely monadic version of the search connections example.
4. More coverage :)

**Use Example:**

```
from linkedin_model import LinkedInPage, EntityType

def con_filter(emp):
    return emp.shared_connections != None and len(emp.shared_connections) > 0

def search_connections(company_name, company_site):

    linked_in = LinkedInPage([mail], [pwd])
    search_results_page = linked_in.search(EntityType.Companies, company_name)
    company_iterator = search_results_page.get_entities_iterator(lambda x: x.name.lower().strip(' ') == company_name)
    refined_search = [ent for ent in company_iterator if ent.web_site == company_site]

    for bee in refined_search:
        company_oage = search_results_page.go_to_result_page(bee)
        company_employees_page = company_oage.go_to_employees_page()
        employees_with_connections = filter(con_filter, company_employees_page.entities_previews)
        linked_in.close()
        return employees_with_connections

```

**Disclaimer:**

Currently, this project is not production ready.