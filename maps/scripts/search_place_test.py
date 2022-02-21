import allure
class TestSearchPlace:
    test_name = "Search Place"
    KPI_COUNT = 2
    test_summary = test_name+" Test Result"

    @allure.title("Google Map Direction Check Test")
    
    
    def test_search_place(self, home):

        home.get_direction()
        

        
        assert self.session_data.KPI_COUNT == self.session_data.pass_count, "Pass Count Failed"

