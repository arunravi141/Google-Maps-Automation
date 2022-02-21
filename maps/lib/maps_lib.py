import kpi_names

def init_timing(self):

    # initialising variables
    self.status = "Fail_launch"
    self.pass_count = 0
    self.fail_count = 0
    self.ADD_KPI_ANNOTATION = True
    self.app_size_info= None
    self.delta_time = 5
    self.connection_status= ""
    self.data_kpi = True
    self.feature = None
    self.debug = False
    self.screenshots = []
    
    # Categories
    self.KPI_LABEL_CATEGORY = "Maps KPI"
    self.genre_id = "Maps Genre"
    

    # KPIs

        
    #Data KPI's
    self.data_kpis = {}  
    self.data_kpis[kpi_names.DIRECTION] = None
   



    # KPI Labels

    self.kpi_labels = {}
    self.kpi_labels[kpi_names.LAUNCH_TIME] = {'start': None, 'end': None}


    # Action Labels
    self.ADD_KPI_ANNOTATION = True
    self.session_start = None
    self.appium_timestamps = {}
    self.action_labels = {}

    return self
