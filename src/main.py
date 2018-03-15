

### main
from src.achieve_urls_from_html import achieve_care_urls_from_index_html, delete_previous_results_file

if __name__ == '__main__':
	search_contents_index_html='http://dblp.uni-trier.de/db/conf/imc/imc2017.html'
	search_contents_index_html = 'http://dblp.uni-trier.de/db/conf/nips/nips2017.html'
	search_contents_index_html='http://dblp.uni-trier.de/db/conf/aaai/aaai2017.html'
	#search_contents_index_html='http://dblp.uni-trier.de/db/conf/ijcai/ijcai2017/.html'

	output_file = search_contents_index_html.split('/')[-1].split('.')[0]+'_ris_result.txt'

	delete_previous_results_file(output_file)
	achieve_care_urls_from_index_html(search_contents_index_html,output_file)
