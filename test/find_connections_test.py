__author__ = 'yoav'

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