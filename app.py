
from flask import (
    Flask,
    render_template,
    request,
    flash
    )
import pandas as pd
import numpy as np
from test_function import test_function
from forms import (
    InputForm,
    output_form,
    DateForm
    )
from input_functions import (
    key_contact_individuals,
    key_contact_individuals_new,
    key_contact_individuals_c3ai,
    LP_input_function,
    LP,
    dashboard_plots,
    
    LP_input_function_c3ai,
    LP_c3ai,
    dashboard_plots_c3ai,
    )
from bokeh.plotting import figure
from bokeh.embed import components
import bokeh
from flask import g
from flask import jsonify
import math
import plotly.graph_objects as go
import plotly

from plotly.offline import iplot, init_notebook_mode
from plotly.subplots import make_subplots
import datetime
import c3aidatalake


app = Flask(__name__)
application = app
app.secret_key = 'sdfjsbs'

counties_dict = {'Mississippi': ['Washington County',
  'Perry County',
  'Choctaw County',
  'Itawamba County',
  'Carroll County',
  'Grenada County',
  'Jefferson County',
  'Greene County',
  'Marshall County',
  'Quitman County',
  'Bolivar County',
  'Lamar County',
  'Lee County',
  'Pike County',
  'Tallahatchie County',
  'Smith County',
  'Stone County',
  'Warren County',
  'Clarke County',
  'Kemper County',
  'Montgomery County',
  'Oktibbeha County',
  'Pearl River County',
  'Leake County',
  'Noxubee County',
  'Neshoba County',
  'Rankin County',
  'Tate County',
  'Lawrence County',
  'Panola County',
  'Yalobusha County',
  'Chickasaw County',
  'Copiah County',
  'George County',
  'Hinds County',
  'Newton County',
  'Union County',
  'Sharkey County',
  'Tippah County',
  'Forrest County',
  'Hancock County',
  'Lafayette County',
  'Issaquena County',
  'Lowndes County',
  'Leflore County',
  'Wilkinson County',
  'Harrison County',
  'Jefferson Davis County',
  'Lincoln County',
  'Scott County',
  'Winston County',
  'Yazoo County',
  'Benton County',
  'Franklin County',
  'Jasper County',
  'Jones County',
  'Monroe County',
  'Sunflower County',
  'Webster County',
  'Adams County',
  'Clay County',
  'Covington County',
  'Humphreys County',
  'Holmes County',
  'Amite County',
  'Calhoun County',
  'Tishomingo County',
  'Wayne County',
  'Madison County',
  'Marion County',
  'Prentiss County',
  'Jackson County',
  'Tunica County',
  'Claiborne County',
  'Lauderdale County',
  'Simpson County',
  'Attala County',
  'Coahoma County',
  'Walthall County',
  'Pontotoc County',
  'Alcorn County',
  'DeSoto County'],
 'Missouri': ['Saline County',
  'Madison County',
  'Wright County',
  'Vernon County',
  'Nodaway County',
  'Chariton County',
  'Grundy County',
  'Morgan County',
  'Wayne County',
  'Bollinger County',
  'Cape Girardeau County',
  'Shelby County',
  'Webster County',
  'Atchison County',
  'Bates County',
  'Benton County',
  'Carter County',
  'Dade County',
  'Linn County',
  'Howell County',
  'Johnson County',
  'Laclede County',
  'Maries County',
  'Phelps County',
  'Platte County',
  'St. Francois County',
  'Andrew County',
  'Carroll County',
  'Daviess County',
  'Knox County',
  'Marion County',
  'Osage County',
  'Ripley County',
  'Warren County',
  'Audrain County',
  'Christian County',
  'Greene County',
  'Harrison County',
  'St. Clair County',
  'Adair County',
  'Scotland County',
  'Sullivan County',
  'Clark County',
  'Jefferson County',
  'Lewis County',
  'New Madrid County',
  'Perry County',
  'Ralls County',
  'Ray County',
  'St. Louis County',
  'Stone County',
  'Barry County',
  'Boone County',
  'Cedar County',
  'Crawford County',
  'Iron County',
  'Livingston County',
  'Moniteau County',
  'Oregon County',
  'Dunklin County',
  'Pettis County',
  'Ste. Genevieve County',
  'Randolph County',
  'Franklin County',
  'Howard County',
  'Jackson County',
  'Miller County',
  'Pulaski County',
  'Putnam County',
  'Taney County',
  'Texas County',
  'Buchanan County',
  'Caldwell County',
  'Callaway County',
  'Cass County',
  'Clinton County',
  'Cooper County',
  'Dallas County',
  'Gentry County',
  'Hickory County',
  'Lincoln County',
  'Mississippi County',
  'Monroe County',
  'Newton County',
  'Ozark County',
  'Pike County',
  'St. Charles County',
  'Mercer County',
  'Clay County',
  'Dent County',
  'Worth County',
  'St. Louis city',
  'Butler County',
  'Holt County',
  'Montgomery County',
  'Stoddard County',
  'Washington County',
  'DeKalb County',
  'Lafayette County',
  'Schuyler County',
  'Camden County',
  'Jasper County',
  'McDonald County',
  'Polk County',
  'Reynolds County',
  'Scott County',
  'Barton County',
  'Cole County',
  'Gasconade County',
  'Macon County',
  'Pemiscot County',
  'Shannon County',
  'Douglas County',
  'Henry County',
  'Lawrence County'],
 'Montana': ['Custer County',
  'Hill County',
  'Powder River County',
  'Park County',
  'Roosevelt County',
  'Blaine County',
  'Liberty County',
  'Richland County',
  'Teton County',
  'Toole County',
  'Fallon County',
  'Daniels County',
  'Judith Basin County',
  'Silver Bow County',
  'Deer Lodge County',
  'Jefferson County',
  'McCone County',
  'Wheatland County',
  'Rosebud County',
  'Carter County',
  'Dawson County',
  'Broadwater County',
  'Lake County',
  'Pondera County',
  'Yellowstone County',
  'Ravalli County',
  'Valley County',
  'Fergus County',
  'Mineral County',
  'Petroleum County',
  'Sanders County',
  'Flathead County',
  'Wibaux County',
  'Meagher County',
  'Carbon County',
  'Phillips County',
  'Chouteau County',
  'Lincoln County',
  'Treasure County',
  'Sweet Grass County',
  'Prairie County',
  'Glacier County',
  'Golden Valley County',
  'Stillwater County',
  'Granite County',
  'Madison County',
  'Sheridan County',
  'Big Horn County',
  'Garfield County',
  'Lewis and Clark County',
  'Missoula County',
  'Cascade County',
  'Powell County',
  'Gallatin County',
  'Beaverhead County',
  'Musselshell County'],
 'Nebraska': ['Adams County',
  'Lancaster County',
  'Boone County',
  'Rock County',
  'Banner County',
  'Sherman County',
  'Richardson County',
  'Howard County',
  'Holt County',
  'Furnas County',
  'Gosper County',
  'Saline County',
  'Sarpy County',
  'Thurston County',
  'Washington County',
  'Boyd County',
  'Cherry County',
  'Dodge County',
  'Fillmore County',
  'Garden County',
  'Hooker County',
  'Morrill County',
  'Nemaha County',
  'Seward County',
  'Thomas County',
  'Dakota County',
  'Webster County',
  'Antelope County',
  'Butler County',
  'Clay County',
  'Custer County',
  'Gage County',
  'Hamilton County',
  'Kearney County',
  'Keith County',
  'Madison County',
  'Perkins County',
  'Saunders County',
  'Wayne County',
  'Keya Paha County',
  'Knox County',
  'Lincoln County',
  'Pierce County',
  'Sioux County',
  'Cass County',
  'Dixon County',
  'Dundy County',
  'Greeley County',
  'Hall County',
  'Otoe County',
  'Red Willow County',
  'Dawes County',
  'Cheyenne County',
  'Dawson County',
  'Valley County',
  'McPherson County',
  'Nance County',
  'Stanton County',
  'Harlan County',
  'Blaine County',
  'Buffalo County',
  'Deuel County',
  'Hitchcock County',
  'Platte County',
  'Thayer County',
  'Box Butte County',
  'Sheridan County',
  'Nuckolls County',
  'Frontier County',
  'Douglas County',
  'Chase County',
  'Arthur County',
  'Franklin County',
  'Jefferson County',
  'Loup County',
  'Phelps County',
  'Scotts Bluff County',
  'Kimball County',
  'Merrick County',
  'Burt County',
  'Cuming County',
  'Grant County',
  'Hayes County',
  'Cedar County',
  'Johnson County',
  'Garfield County',
  'Pawnee County',
  'Wheeler County',
  'York County',
  'Colfax County',
  'Logan County',
  'Polk County',
  'Brown County'],
 'Nevada': ['Churchill County',
  'Douglas County',
  'Pershing County',
  'Esmeralda County',
  'Humboldt County',
  'Mineral County',
  'White Pine County',
  'Elko County',
  'Lincoln County',
  'Nye County',
  'Storey County',
  'Washoe County',
  'Clark County',
  'Carson City',
  'Lyon County',
  'Lander County',
  'Eureka County'],
 'New Hampshire': ['Cheshire County',
  'Merrimack County',
  'Grafton County',
  'Rockingham County',
  'Belknap County',
  'Sullivan County',
  'Hillsborough County',
  'Strafford County',
  'Coos County',
  'Carroll County'],
 'New Jersey': ['Monmouth County',
  'Sussex County',
  'Cumberland County',
  'Essex County',
  'Ocean County',
  'Gloucester County',
  'Salem County',
  'Passaic County',
  'Camden County',
  'Bergen County',
  'Warren County',
  'Hudson County',
  'Burlington County',
  'Morris County',
  'Mercer County',
  'Somerset County',
  'Atlantic County',
  'Middlesex County',
  'Cape May County',
  'Union County',
  'Hunterdon County'],
 'New Mexico': ['Rio Arriba County',
  'San Miguel County',
  'Torrance County',
  'Otero County',
  'Cibola County',
  'Guadalupe County',
  'Catron County',
  'Grant County',
  'Luna County',
  'McKinley County',
  'Taos County',
  'Colfax County',
  'Eddy County',
  'Mora County',
  'Quay County',
  'Lincoln County',
  'Lea County',
  'Santa Fe County',
  'Sierra County',
  'Socorro County',
  'Do�a Ana County',
  'Los Alamos County',
  'Valencia County',
  'Bernalillo County',
  'De Baca County',
  'Hidalgo County',
  'Sandoval County',
  'Curry County',
  'Harding County',
  'San Juan County',
  'Chaves County',
  'Union County',
  'Roosevelt County'],
 'New York': ['Schoharie County',
  'Onondaga County',
  'Clinton County',
  'Seneca County',
  'Putnam County',
  'Franklin County',
  'Ontario County',
  'Queens County',
  'Steuben County',
  'Hamilton County',
  'Washington County',
  'Chautauqua County',
  'Kings County',
  'New York County',
  'Tioga County',
  'Cayuga County',
  'Orleans County',
  'Saratoga County',
  'Rockland County',
  'Columbia County',
  'Lewis County',
  'Niagara County',
  'Westchester County',
  'Delaware County',
  'Essex County',
  'Montgomery County',
  'Nassau County',
  'Richmond County',
  'Schuyler County',
  'Tompkins County',
  'Chenango County',
  'Cortland County',
  'Jefferson County',
  'Oneida County',
  'Suffolk County',
  'Wyoming County',
  'Chemung County',
  'Oswego County',
  'Otsego County',
  'Wayne County',
  'Albany County',
  'Broome County',
  'Erie County',
  'Madison County',
  'Sullivan County',
  'Genesee County',
  'Orange County',
  'Bronx County',
  'Fulton County',
  'Rensselaer County',
  'Dutchess County',
  'Herkimer County',
  'St. Lawrence County',
  'Warren County',
  'Monroe County',
  'Ulster County',
  'Livingston County',
  'Greene County',
  'Allegany County',
  'Cattaraugus County',
  'Schenectady County',
  'Yates County'],
 'North Carolina': ['Mitchell County',
  'Greene County',
  'Chowan County',
  'Caldwell County',
  'Catawba County',
  'Craven County',
  'Edgecombe County',
  'Harnett County',
  'Henderson County',
  'Hyde County',
  'Mecklenburg County',
  'Northampton County',
  'Rowan County',
  'Vance County',
  'Currituck County',
  'Union County',
  'Forsyth County',
  'Nash County',
  'Bladen County',
  'Dare County',
  'Warren County',
  'Wilson County',
  'Bertie County',
  'Gates County',
  'Graham County',
  'Martin County',
  'Madison County',
  'Pamlico County',
  'Perquimans County',
  'Polk County',
  'Randolph County',
  'Rockingham County',
  'Stokes County',
  'Washington County',
  'Camden County',
  'Clay County',
  'Cumberland County',
  'Gaston County',
  'Guilford County',
  'Jackson County',
  'Moore County',
  'Robeson County',
  'Stanly County',
  'Wake County',
  'Yancey County',
  'Chatham County',
  'McDowell County',
  'Johnston County',
  'Jones County',
  'Person County',
  'Brunswick County',
  'Ashe County',
  'Beaufort County',
  'Lenoir County',
  'Rutherford County',
  'Lincoln County',
  'Onslow County',
  'Orange County',
  'Sampson County',
  'Yadkin County',
  'Avery County',
  'Burke County',
  'Caswell County',
  'Davie County',
  'Duplin County',
  'Durham County',
  'Lee County',
  'New Hanover County',
  'Wayne County',
  'Scotland County',
  'Halifax County',
  'Alamance County',
  'Haywood County',
  'Alleghany County',
  'Cleveland County',
  'Granville County',
  'Hoke County',
  'Iredell County',
  'Pitt County',
  'Cherokee County',
  'Wilkes County',
  'Alexander County',
  'Carteret County',
  'Pasquotank County',
  'Swain County',
  'Anson County',
  'Franklin County',
  'Macon County',
  'Transylvania County',
  'Columbus County',
  'Montgomery County',
  'Richmond County',
  'Surry County',
  'Buncombe County',
  'Cabarrus County',
  'Davidson County',
  'Hertford County',
  'Pender County',
  'Watauga County',
  'Tyrrell County'],
 'North Dakota': ['Burke County',
  'Mountrail County',
  'Williams County',
  'Billings County',
  'Kidder County',
  'Cavalier County',
  'Grant County',
  'Pembina County',
  'Steele County',
  'Hettinger County',
  'LaMoure County',
  'Morton County',
  'Cass County',
  'Dunn County',
  'Emmons County',
  'McIntosh County',
  'Nelson County',
  'Richland County',
  'Rolette County',
  'Walsh County',
  'Adams County',
  'Bottineau County',
  'Barnes County',
  'Eddy County',
  'Grand Forks County',
  'McKenzie County',
  'Mercer County',
  'McLean County',
  'Pierce County',
  'Ransom County',
  'Sioux County',
  'Bowman County',
  'Golden Valley County',
  'Logan County',
  'Towner County',
  'Stutsman County',
  'Divide County',
  'Foster County',
  'Sargent County',
  'Slope County',
  'Stark County',
  'Traill County',
  'Dickey County',
  'Ward County',
  'McHenry County',
  'Benson County',
  'Renville County',
  'Burleigh County',
  'Oliver County',
  'Ramsey County',
  'Griggs County',
  'Sheridan County',
  'Wells County'],
 'Ohio': ['Gallia County',
  'Huron County',
  'Athens County',
  'Adams County',
  'Medina County',
  'Union County',
  'Champaign County',
  'Paulding County',
  'Greene County',
  'Franklin County',
  'Marion County',
  'Morgan County',
  'Wayne County',
  'Wyandot County',
  'Butler County',
  'Harrison County',
  'Knox County',
  'Richland County',
  'Vinton County',
  'Hancock County',
  'Fairfield County',
  'Defiance County',
  'Henry County',
  'Jefferson County',
  'Putnam County',
  'Clinton County',
  'Fayette County',
  'Pickaway County',
  'Logan County',
  'Summit County',
  'Sandusky County',
  'Shelby County',
  'Van Wert County',
  'Washington County',
  'Williams County',
  'Auglaize County',
  'Columbiana County',
  'Darke County',
  'Ottawa County',
  'Fulton County',
  'Hardin County',
  'Jackson County',
  'Lucas County',
  'Morrow County',
  'Noble County',
  'Preble County',
  'Seneca County',
  'Stark County',
  'Allen County',
  'Coshocton County',
  'Crawford County',
  'Delaware County',
  'Guernsey County',
  'Hocking County',
  'Mercer County',
  'Ross County',
  'Cuyahoga County',
  'Lorain County',
  'Miami County',
  'Montgomery County',
  'Trumbull County',
  'Wood County',
  'Ashtabula County',
  'Madison County',
  'Muskingum County',
  'Geauga County',
  'Monroe County',
  'Lake County',
  'Clark County',
  'Holmes County',
  'Warren County',
  'Ashland County',
  'Mahoning County',
  'Scioto County',
  'Meigs County',
  'Pike County',
  'Hamilton County',
  'Erie County',
  'Lawrence County',
  'Tuscarawas County',
  'Brown County',
  'Licking County',
  'Carroll County',
  'Clermont County',
  'Highland County',
  'Portage County',
  'Belmont County',
  'Perry County'],
 'Minnesota': ['Cottonwood County',
  'Scott County',
  'Dodge County',
  'Wabasha County',
  'Pipestone County',
  'Crow Wing County',
  'Norman County',
  'Wright County',
  'Nicollet County',
  'Douglas County',
  'Grant County',
  'Kittson County',
  'Le Sueur County',
  'Mahnomen County',
  'Chisago County',
  'Redwood County',
  'Yellow Medicine County',
  'Todd County',
  'Beltrami County',
  'Blue Earth County',
  'Houston County',
  'Lac qui Parle County',
  'Lake of the Woods County',
  'Otter Tail County',
  'Waseca County',
  'St. Louis County',
  'Anoka County',
  'Stearns County',
  'Lincoln County',
  'Marshall County',
  'Mille Lacs County',
  'Washington County',
  'Carlton County',
  'Kanabec County',
  'Koochiching County',
  'Red Lake County',
  'Morrison County',
  'Rice County',
  'Steele County',
  'Aitkin County',
  'Faribault County',
  'Murray County',
  'Kandiyohi County',
  'Lake County',
  'Rock County',
  'Sibley County',
  'Traverse County',
  'Becker County',
  'Hennepin County',
  'Brown County',
  'Chippewa County',
  'Clearwater County',
  'Hubbard County',
  'Isanti County',
  'Martin County',
  'Mower County',
  'Pine County',
  'Olmsted County',
  'Wadena County',
  'Benton County',
  'Freeborn County',
  'McLeod County',
  'Pope County',
  'Stevens County',
  'Swift County',
  'Dakota County',
  'Lyon County',
  'Renville County',
  'Cook County',
  'Meeker County',
  'Pennington County',
  'Wilkin County',
  'Clay County',
  'Fillmore County',
  'Polk County',
  'Roseau County',
  'Watonwan County',
  'Big Stone County',
  'Cass County',
  'Goodhue County',
  'Jackson County',
  'Nobles County',
  'Sherburne County',
  'Carver County',
  'Itasca County',
  'Ramsey County',
  'Winona County'],
 'Texas': ['Austin County',
  'Kenedy County',
  'Nueces County',
  'Colorado County',
  'San Patricio County',
  'Rains County',
  'Randall County',
  'Real County',
  'San Saba County',
  'Schleicher County',
  'Sterling County',
  'Zavala County',
  'Calhoun County',
  'Carson County',
  'Foard County',
  'Freestone County',
  'Goliad County',
  'Hamilton County',
  'Hardeman County',
  'Mitchell County',
  'Briscoe County',
  'Lavaca County',
  'Terry County',
  'Jeff Davis County',
  'Webb County',
  'Jim Hogg County',
  'Montgomery County',
  'Dallam County',
  'Armstrong County',
  'Castro County',
  'Kleberg County',
  'Willacy County',
  'Crosby County',
  'Fisher County',
  'Duval County',
  'Blanco County',
  'Jasper County',
  'Kinney County',
  'Deaf Smith County',
  'Galveston County',
  'La Salle County',
  'Roberts County',
  'Tyler County',
  'Wheeler County',
  'Bowie County',
  'Brewster County',
  'Kent County',
  'Smith County',
  'Crockett County',
  'Hardin County',
  'Howard County',
  'Leon County',
  'Montague County',
  'Panola County',
  'Erath County',
  'Brazoria County',
  'Motley County',
  'Donley County',
  'Atascosa County',
  'Coleman County',
  'Nolan County',
  'Hudspeth County',
  'Medina County',
  'Ward County',
  'Henderson County',
  'Harrison County',
  'Menard County',
  'Lamar County',
  'Fayette County',
  'Williamson County',
  'Polk County',
  'Refugio County',
  'Caldwell County',
  'Wilbarger County',
  'Reagan County',
  'Hale County',
  'Shelby County',
  'Runnels County',
  'San Jacinto County',
  'Tom Green County',
  'Victoria County',
  'Waller County',
  'Wichita County',
  'Wilson County',
  'Hockley County',
  'Maverick County',
  'Fannin County',
  'Midland County',
  'Live Oak County',
  'Llano County',
  'Karnes County',
  'Brazos County',
  'Cass County',
  'Gaines County',
  'Gray County',
  'Madison County',
  'Jack County',
  'Kendall County',
  'Bosque County',
  'Bexar County',
  'Bailey County',
  'Baylor County',
  'Cameron County',
  'Denton County',
  'Washington County',
  'Morris County',
  'Stephens County',
  'Harris County',
  'Andrews County',
  'Gillespie County',
  'Gonzales County',
  'Lynn County',
  'Young County',
  'Zapata County',
  'Hood County',
  'Hopkins County',
  'Ochiltree County',
  'King County',
  'Knox County',
  'McLennan County',
  'Cherokee County',
  'Concho County',
  'Delta County',
  'Edwards County',
  'Eastland County',
  'Jones County',
  'Reeves County',
  'Sabine County',
  'Sherman County',
  'Swisher County',
  'Hunt County',
  'Camp County',
  'Hansford County',
  'Guadalupe County',
  'Clay County',
  'Hill County',
  'Nacogdoches County',
  'Parmer County',
  'Presidio County',
  'Val Verde County',
  'Ector County',
  'Glasscock County',
  'Grimes County',
  'Collin County',
  'Angelina County',
  'Cottle County',
  'Hays County',
  'Rockwall County',
  'Lipscomb County',
  'Matagorda County',
  'Pecos County',
  'Rusk County',
  'Throckmorton County',
  'Walker County',
  'Wood County',
  'Aransas County',
  'Childress County',
  'Coke County',
  'Coryell County',
  'Hemphill County',
  'Moore County',
  'Navarro County',
  'San Augustine County',
  'Shackelford County',
  'Starr County',
  'Upton County',
  'Bastrop County',
  'Hall County',
  'Franklin County',
  'Frio County',
  'Lampasas County',
  'Mason County',
  'Dickens County',
  'Tarrant County',
  'Anderson County',
  'Jackson County',
  'Milam County',
  'Comanche County',
  'Brooks County',
  'Titus County',
  'Liberty County',
  'Wise County',
  'Jim Wells County',
  'Dimmit County',
  'Fort Bend County',
  'Irion County',
  'Cooke County',
  'Dawson County',
  'Burleson County',
  'Jefferson County',
  'Oldham County',
  'El Paso County',
  'Terrell County',
  'Uvalde County',
  'Archer County',
  'Hidalgo County',
  'Somervell County',
  'Haskell County',
  'Mills County',
  'Newton County',
  'Martin County',
  'Kimble County',
  'Van Zandt County',
  'Yoakum County',
  'Red River County',
  'Sutton County',
  'Upshur County',
  'Wharton County',
  'Borden County',
  'Marion County',
  'Grayson County',
  'Palo Pinto County',
  'DeWitt County',
  'Callahan County',
  'Gregg County',
  'Lubbock County',
  'Kaufman County',
  'Floyd County',
  'Chambers County',
  'Bell County',
  'Hutchinson County',
  'Orange County',
  'Winkler County',
  'Burnet County',
  'Dallas County',
  'McMullen County',
  'Johnson County',
  'Hartley County',
  'Limestone County',
  'Parker County',
  'Culberson County',
  'Garza County',
  'Travis County',
  'Collingsworth County',
  'Lamb County',
  'Loving County',
  'Bandera County',
  'Robertson County',
  'Taylor County',
  'Trinity County',
  'Cochran County',
  'Comal County',
  'Houston County',
  'Potter County',
  'Scurry County',
  'Crane County',
  'Stonewall County',
  'Brown County',
  'Bee County',
  'McCulloch County',
  'Lee County',
  'Ellis County',
  'Kerr County',
  'Falls County'],
 'Utah': ['Millard County',
  'Washington County',
  'Kane County',
  'Grand County',
  'Rich County',
  'Wasatch County',
  'Box Elder County',
  'Iron County',
  'Sevier County',
  'Weber County',
  'Duchesne County',
  'San Juan County',
  'Salt Lake County',
  'Uintah County',
  'Daggett County',
  'Davis County',
  'Wayne County',
  'Carbon County',
  'Emery County',
  'Morgan County',
  'Cache County',
  'Garfield County',
  'Juab County',
  'Tooele County',
  'Summit County',
  'Piute County',
  'Beaver County',
  'Sanpete County',
  'Utah County'],
 'Vermont': ['Rutland County',
  'Orleans County',
  'Grand Isle County',
  'Orange County',
  'Chittenden County',
  'Lamoille County',
  'Windsor County',
  'Caledonia County',
  'Windham County',
  'Addison County',
  'Washington County',
  'Franklin County',
  'Bennington County',
  'Essex County'],
 'Virginia': ['Tazewell County',
  'Falls Church city',
  'Manassas Park city',
  'Poquoson city',
  'Sussex County',
  'Waynesboro city',
  'Roanoke city',
  'Salem city',
  'Norfolk city',
  'Charlotte County',
  'Fairfax County',
  'Greensville County',
  'James City County',
  'Russell County',
  'Smyth County',
  'Lexington city',
  'Campbell County',
  'Henry County',
  'King George County',
  'Lancaster County',
  'Lee County',
  'Mathews County',
  'Middlesex County',
  'Prince George County',
  'Rockingham County',
  'Scott County',
  'Surry County',
  'Appomattox County',
  'Franklin County',
  'King and Queen County',
  'Montgomery County',
  'New Kent County',
  'Cumberland County',
  'Goochland County',
  'Halifax County',
  'Madison County',
  'Prince William County',
  'Southampton County',
  'Highland County',
  'Brunswick County',
  'Caroline County',
  'Gloucester County',
  'Northampton County',
  'Patrick County',
  'Powhatan County',
  'Rockbridge County',
  'Shenandoah County',
  'Fauquier County',
  'Charles City County',
  'Culpeper County',
  'Dinwiddie County',
  'Greene County',
  'Hanover County',
  'Lunenburg County',
  'Orange County',
  'Harrisonburg city',
  'Emporia city',
  'Wythe County',
  'Chesapeake city',
  'Albemarle County',
  'Bedford County',
  'Botetourt County',
  'Wise County',
  'Bristol city',
  'Portsmouth city',
  'Williamsburg city',
  'Alleghany County',
  'Carroll County',
  'Washington County',
  'Northumberland County',
  'Page County',
  'Warren County',
  'Alexandria city',
  'Fredericksburg city',
  'Hampton city',
  'Arlington County',
  'Hopewell city',
  'Buchanan County',
  'Frederick County',
  'Stafford County',
  'York County',
  'Richmond city',
  'Nelson County',
  'Pittsylvania County',
  'Norton city',
  'Fluvanna County',
  'Amelia County',
  'Winchester city',
  'Accomack County',
  'Floyd County',
  'Grayson County',
  'Nottoway County',
  'Buena Vista city',
  'Petersburg city',
  'Fairfax city',
  'Manassas city',
  'Suffolk city',
  'Chesterfield County',
  'Isle of Wight County',
  'Franklin city',
  'Charlottesville city',
  'Henrico County',
  'King William County',
  'Louisa County',
  'Prince Edward County',
  'Richmond County',
  'Spotsylvania County',
  'Clarke County',
  'Mecklenburg County',
  'Augusta County',
  'Dickenson County',
  'Loudoun County',
  'Roanoke County',
  'Colonial Heights city',
  'Bland County',
  'Buckingham County',
  'Covington city',
  'Virginia Beach city',
  'Galax city',
  'Westmoreland County',
  'Pulaski County',
  'Danville city',
  'Amherst County',
  'Bath County',
  'Newport News city',
  'Lynchburg city',
  'Martinsville city',
  'Essex County',
  'Staunton city',
  'Radford city',
  'Craig County',
  'Giles County',
  'Rappahannock County'],
 'West Virginia': ['Harrison County',
  'Ohio County',
  'Calhoun County',
  'Morgan County',
  'Raleigh County',
  'Braxton County',
  'Barbour County',
  'McDowell County',
  'Wayne County',
  'Wyoming County',
  'Jackson County',
  'Mercer County',
  'Upshur County',
  'Webster County',
  'Berkeley County',
  'Fayette County',
  'Grant County',
  'Hampshire County',
  'Summers County',
  'Brooke County',
  'Doddridge County',
  'Mineral County',
  'Greenbrier County',
  'Hardy County',
  'Marion County',
  'Mingo County',
  'Hancock County',
  'Lewis County',
  'Nicholas County',
  'Pocahontas County',
  'Tyler County',
  'Randolph County',
  'Taylor County',
  'Wirt County',
  'Clay County',
  'Gilmer County',
  'Monongalia County',
  'Monroe County',
  'Wetzel County',
  'Cabell County',
  'Kanawha County',
  'Pendleton County',
  'Preston County',
  'Ritchie County',
  'Lincoln County',
  'Putnam County',
  'Boone County',
  'Marshall County',
  'Tucker County',
  'Pleasants County',
  'Roane County',
  'Wood County',
  'Mason County',
  'Jefferson County',
  'Logan County'],
 'Washington': ['Kitsap County',
  'King County',
  'Pend Oreille County',
  'San Juan County',
  'Whitman County',
  'Yakima County',
  'Cowlitz County',
  'Ferry County',
  'Lewis County',
  'Grays Harbor County',
  'Island County',
  'Wahkiakum County',
  'Franklin County',
  'Grant County',
  'Whatcom County',
  'Okanogan County',
  'Kittitas County',
  'Benton County',
  'Columbia County',
  'Asotin County',
  'Garfield County',
  'Mason County',
  'Stevens County',
  'Spokane County',
  'Chelan County',
  'Jefferson County',
  'Pacific County',
  'Skamania County',
  'Clallam County',
  'Klickitat County',
  'Douglas County',
  'Pierce County',
  'Walla Walla County',
  'Snohomish County',
  'Thurston County',
  'Clark County',
  'Adams County',
  'Skagit County',
  'Lincoln County'],
 'Wisconsin': ['Rock County',
  'Waushara County',
  'Adams County',
  'Bayfield County',
  'Lafayette County',
  'Monroe County',
  'Pierce County',
  'Wood County',
  'Ashland County',
  'Calumet County',
  'Florence County',
  'Clark County',
  'Jefferson County',
  'Kenosha County',
  'Iron County',
  'St. Croix County',
  'Oconto County',
  'Lincoln County',
  'Waupaca County',
  'Barron County',
  'Sawyer County',
  'Green Lake County',
  'Marquette County',
  'Marinette County',
  'Racine County',
  'Winnebago County',
  'Forest County',
  'Grant County',
  'Rusk County',
  'Sheboygan County',
  'Langlade County',
  'Outagamie County',
  'Vernon County',
  'Columbia County',
  'Kewaunee County',
  'Brown County',
  'Marathon County',
  'Oneida County',
  'Trempealeau County',
  'Washburn County',
  'Dodge County',
  'Walworth County',
  'Crawford County',
  'Manitowoc County',
  'Sauk County',
  'Burnett County',
  'Chippewa County',
  'Door County',
  'Douglas County',
  'Jackson County',
  'Iowa County',
  'Ozaukee County',
  'Richland County',
  'Taylor County',
  'Price County',
  'Milwaukee County',
  'Dunn County',
  'Green County',
  'Shawano County',
  'Menominee County',
  'Buffalo County',
  'La Crosse County',
  'Eau Claire County',
  'Polk County',
  'Waukesha County',
  'Vilas County',
  'Juneau County',
  'Washington County',
  'Dane County',
  'Fond du Lac County',
  'Pepin County',
  'Portage County'],
 'Wyoming': ['Campbell County',
  'Johnson County',
  'Natrona County',
  'Converse County',
  'Niobrara County',
  'Teton County',
  'Sweetwater County',
  'Platte County',
  'Park County',
  'Sheridan County',
  'Big Horn County',
  'Crook County',
  'Albany County',
  'Carbon County',
  'Goshen County',
  'Uinta County',
  'Washakie County',
  'Hot Springs County',
  'Fremont County',
  'Sublette County',
  'Weston County',
  'Lincoln County',
  'Laramie County'],
 'Puerto Rico': ['Hatillo Municipio',
  'Humacao Municipio',
  'Morovis Municipio',
  'Mayag�ez Municipio',
  'Trujillo Alto Municipio',
  'Quebradillas Municipio',
  'Moca Municipio',
  'Culebra Municipio',
  'Salinas Municipio',
  'Barceloneta Municipio',
  'Yauco Municipio',
  'Guaynabo Municipio',
  'Cabo Rojo Municipio',
  'Fajardo Municipio',
  'Patillas Municipio',
  'Rinc�n Municipio',
  'Aguas Buenas Municipio',
  'Bayam�n Municipio',
  'Cayey Municipio',
  'Maunabo Municipio',
  'Pe�uelas Municipio',
  'San Sebasti�n Municipio',
  'Toa Alta Municipio',
  'Vieques Municipio',
  'Yabucoa Municipio',
  'Caguas Municipio',
  'Can�vanas Municipio',
  'Coamo Municipio',
  'Dorado Municipio',
  'Barranquitas Municipio',
  'Orocovis Municipio',
  'A�asco Municipio',
  'Ceiba Municipio',
  'Comer�o Municipio',
  'Isabela Municipio',
  'Lares Municipio',
  'Las Piedras Municipio',
  'San Juan Municipio',
  'Vega Alta Municipio',
  'Maricao Municipio',
  'Aibonito Municipio',
  'Juncos Municipio',
  'Sabana Grande Municipio',
  'Hormigueros Municipio',
  'Adjuntas Municipio',
  'Camuy Municipio',
  'Gu�nica Municipio',
  'Manat� Municipio',
  'Naguabo Municipio',
  'Naranjito Municipio',
  'San Germ�n Municipio',
  'Utuado Municipio',
  'Arecibo Municipio',
  'Arroyo Municipio',
  'Cata�o Municipio',
  'Florida Municipio',
  'Juana D�az Municipio',
  'Santa Isabel Municipio',
  'Guayama Municipio',
  'Gurabo Municipio',
  'Lo�za Municipio',
  'Aguadilla Municipio',
  'Las Mar�as Municipio',
  'Villalba Municipio',
  'Carolina Municipio',
  'Corozal Municipio',
  'Ponce Municipio',
  'Toa Baja Municipio',
  'Aguada Municipio',
  'Ciales Municipio',
  'Cidra Municipio',
  'Luquillo Municipio',
  'San Lorenzo Municipio',
  'Jayuya Municipio',
  'R�o Grande Municipio',
  'Vega Baja Municipio',
  'Guayanilla Municipio',
  'Lajas Municipio'],
 'Alabama': ['Monroe County',
  'Lawrence County',
  'Lee County',
  'Pickens County',
  'Sumter County',
  'Choctaw County',
  'Marengo County',
  'Russell County',
  'Covington County',
  'Crenshaw County',
  'Lauderdale County',
  'Lowndes County',
  'Limestone County',
  'St. Clair County',
  'Winston County',
  'Cullman County',
  'Elmore County',
  'Jackson County',
  'Talladega County',
  'Washington County',
  'Coffee County',
  'Morgan County',
  'Chilton County',
  'Colbert County',
  'Dale County',
  'Etowah County',
  'DeKalb County',
  'Lamar County',
  'Randolph County',
  'Mobile County',
  'Walker County',
  'Cleburne County',
  'Greene County',
  'Barbour County',
  'Bullock County',
  'Calhoun County',
  'Clarke County',
  'Montgomery County',
  'Marshall County',
  'Henry County',
  'Madison County',
  'Tallapoosa County',
  'Wilcox County',
  'Marion County',
  'Jefferson County',
  'Franklin County',
  'Cherokee County',
  'Dallas County',
  'Macon County',
  'Shelby County',
  'Baldwin County',
  'Houston County',
  'Tuscaloosa County',
  'Clay County',
  'Pike County',
  'Coosa County',
  'Hale County',
  'Escambia County',
  'Butler County',
  'Perry County',
  'Conecuh County',
  'Bibb County',
  'Chambers County',
  'Fayette County',
  'Blount County',
  'Autauga County',
  'Geneva County'],
 'Alaska': ['Aleutians West Census Area',
  'Denali Borough',
  'Kenai Peninsula Borough',
  'Bristol Bay Borough',
  'Kodiak Island Borough',
  'Northwest Arctic Borough',
  'Bethel Census Area',
  'North Slope Borough',
  'Sitka City and Borough',
  'Fairbanks North Star Borough',
  'Ketchikan Gateway Borough',
  'Matanuska-Susitna Borough',
  'Nome Census Area',
  'Dillingham Census Area',
  'Haines Borough',
  'Yakutat City and Borough',
  'Juneau City and Borough',
  'Lake and Peninsula Borough',
  'Southeast Fairbanks Census Area',
  'Yukon-Koyukuk Census Area',
  'Anchorage Municipality',
  'Aleutians East Borough',
  'Skagway Municipality',
  'Prince of Wales-Hyder Census Area',
  'Petersburg Borough',
  'Kusilvak Census Area',
  'Valdez-Cordova Census Area',
  'Hoonah-Angoon Census Area',
  'Wrangell City and Borough'],
 'Arizona': ['Maricopa County',
  'Graham County',
  'Santa Cruz County',
  'La Paz County',
  'Mohave County',
  'Coconino County',
  'Yuma County',
  'Greenlee County',
  'Pinal County',
  'Pima County',
  'Gila County',
  'Cochise County',
  'Apache County',
  'Yavapai County',
  'Navajo County'],
 'Arkansas': ['St. Francis County',
  'White County',
  'Nevada County',
  'Cross County',
  'Drew County',
  'Columbia County',
  'Saline County',
  'Van Buren County',
  'Izard County',
  'Lincoln County',
  'Logan County',
  'Crittenden County',
  'Franklin County',
  'Pike County',
  'Jefferson County',
  'Montgomery County',
  'Scott County',
  'Sebastian County',
  'Benton County',
  'Chicot County',
  'Johnson County',
  'Lee County',
  'Pope County',
  'Desha County',
  'Fulton County',
  'Garland County',
  'Prairie County',
  'Woodruff County',
  'Cleburne County',
  'Cleveland County',
  'Jackson County',
  'Hempstead County',
  'Sharp County',
  'Stone County',
  'Washington County',
  'Baxter County',
  'Ashley County',
  'Craighead County',
  'Greene County',
  'Lafayette County',
  'Perry County',
  'Phillips County',
  'Poinsett County',
  'Sevier County',
  'Yell County',
  'Calhoun County',
  'Clark County',
  'Bradley County',
  'Monroe County',
  'Polk County',
  'Ouachita County',
  'Newton County',
  'Little River County',
  'Carroll County',
  'Miller County',
  'Pulaski County',
  'Clay County',
  'Dallas County',
  'Randolph County',
  'Boone County',
  'Independence County',
  'Grant County',
  'Faulkner County',
  'Marion County',
  'Searcy County',
  'Crawford County',
  'Hot Spring County',
  'Madison County',
  'Howard County',
  'Mississippi County',
  'Union County',
  'Lawrence County',
  'Conway County',
  'Arkansas County',
  'Lonoke County'],
 'Oklahoma': ['Adair County',
  'Stephens County',
  'Cimarron County',
  'Carter County',
  'Grant County',
  'Greer County',
  'McClain County',
  'McIntosh County',
  'Murray County',
  'Noble County',
  'Ottawa County',
  'Sequoyah County',
  'Wagoner County',
  'Woods County',
  'Caddo County',
  'Muskogee County',
  'Okfuskee County',
  'Bryan County',
  'Harper County',
  'Kay County',
  'Craig County',
  'Tulsa County',
  'Canadian County',
  'Harmon County',
  'Pushmataha County',
  'Latimer County',
  'Osage County',
  'Texas County',
  'Garfield County',
  'Johnston County',
  'Pittsburg County',
  'Roger Mills County',
  'Woodward County',
  'Cherokee County',
  'Delaware County',
  'Ellis County',
  'Grady County',
  'Payne County',
  'Pottawatomie County',
  'Creek County',
  'Tillman County',
  'Washita County',
  'Cotton County',
  'Kiowa County',
  'Le Flore County',
  'McCurtain County',
  'Major County',
  'Mayes County',
  'Oklahoma County',
  'Custer County',
  'Beaver County',
  'Love County',
  'Beckham County',
  'Choctaw County',
  'Jackson County',
  'Lincoln County',
  'Seminole County',
  'Blaine County',
  'Coal County',
  'Kingfisher County',
  'Marshall County',
  'Nowata County',
  'Rogers County',
  'Alfalfa County',
  'Cleveland County',
  'Atoka County',
  'Dewey County',
  'Logan County',
  'Washington County',
  'Haskell County',
  'Okmulgee County',
  'Jefferson County',
  'Garvin County',
  'Pontotoc County',
  'Hughes County',
  'Comanche County',
  'Pawnee County'],
 'Oregon': ['Marion County',
  'Jackson County',
  'Grant County',
  'Jefferson County',
  'Clackamas County',
  'Linn County',
  'Tillamook County',
  'Baker County',
  'Josephine County',
  'Umatilla County',
  'Lincoln County',
  'Columbia County',
  'Sherman County',
  'Wasco County',
  'Lane County',
  'Malheur County',
  'Washington County',
  'Morrow County',
  'Clatsop County',
  'Curry County',
  'Gilliam County',
  'Lake County',
  'Union County',
  'Douglas County',
  'Polk County',
  'Deschutes County',
  'Yamhill County',
  'Klamath County',
  'Benton County',
  'Crook County',
  'Harney County',
  'Wallowa County',
  'Wheeler County',
  'Coos County',
  'Hood River County',
  'Multnomah County'],
 'Pennsylvania': ['Delaware County',
  'Union County',
  'Wayne County',
  'Dauphin County',
  'Westmoreland County',
  'Forest County',
  'Monroe County',
  'Philadelphia County',
  'Blair County',
  'Cambria County',
  'Berks County',
  'Huntingdon County',
  'Lawrence County',
  'Mifflin County',
  'Cumberland County',
  'Allegheny County',
  'Snyder County',
  'Susquehanna County',
  'Crawford County',
  'Erie County',
  'Fulton County',
  'Juniata County',
  'Schuylkill County',
  'Wyoming County',
  'Adams County',
  'Armstrong County',
  'Clinton County',
  'Carbon County',
  'Centre County',
  'Northumberland County',
  'Northampton County',
  'Cameron County',
  'Venango County',
  'Beaver County',
  'Bucks County',
  'Lackawanna County',
  'McKean County',
  'Fayette County',
  'Montgomery County',
  'Greene County',
  'Lebanon County',
  'Luzerne County',
  'Montour County',
  'Columbia County',
  'Butler County',
  'Jefferson County',
  'Lancaster County',
  'Perry County',
  'Potter County',
  'Tioga County',
  'Franklin County',
  'Bedford County',
  'Somerset County',
  'York County',
  'Bradford County',
  'Chester County',
  'Indiana County',
  'Washington County',
  'Pike County',
  'Lehigh County',
  'Clarion County',
  'Clearfield County',
  'Lycoming County',
  'Warren County',
  'Elk County',
  'Mercer County',
  'Sullivan County'],
 'Rhode Island': ['Providence County',
  'Bristol County',
  'Newport County',
  'Kent County',
  'Washington County'],
 'South Carolina': ['Aiken County',
  'Newberry County',
  'Edgefield County',
  'Clarendon County',
  'Colleton County',
  'Sumter County',
  'Lexington County',
  'Barnwell County',
  'York County',
  'Berkeley County',
  'Darlington County',
  'Georgetown County',
  'Anderson County',
  'Chesterfield County',
  'Greenwood County',
  'Horry County',
  'Kershaw County',
  'Orangeburg County',
  'Abbeville County',
  'Bamberg County',
  'Calhoun County',
  'Dillon County',
  'Richland County',
  'Fairfield County',
  'Hampton County',
  'Greenville County',
  'Lancaster County',
  'Dorchester County',
  'Florence County',
  'Laurens County',
  'McCormick County',
  'Pickens County',
  'Union County',
  'Williamsburg County',
  'Oconee County',
  'Allendale County',
  'Chester County',
  'Marion County',
  'Charleston County',
  'Marlboro County',
  'Cherokee County',
  'Jasper County',
  'Lee County',
  'Spartanburg County',
  'Beaufort County',
  'Saluda County'],
 'South Dakota': ['Aurora County',
  'Grant County',
  'Tripp County',
  'Jackson County',
  'Minnehaha County',
  'Custer County',
  'Hyde County',
  'Clark County',
  'Faulk County',
  'Kingsbury County',
  'Walworth County',
  'Clay County',
  'Day County',
  'Douglas County',
  'Harding County',
  'McPherson County',
  'Roberts County',
  'Sully County',
  'Lincoln County',
  'Lake County',
  'Lawrence County',
  'Codington County',
  'Butte County',
  'Corson County',
  'Edmunds County',
  'Campbell County',
  'Bennett County',
  'Haakon County',
  'Jones County',
  'Meade County',
  'McCook County',
  'Turner County',
  'Brown County',
  'Hanson County',
  'Mellette County',
  'Perkins County',
  'Pennington County',
  'Union County',
  'Miner County',
  'Ziebach County',
  'Deuel County',
  'Bon Homme County',
  'Brule County',
  'Fall River County',
  'Gregory County',
  'Oglala Lakota County',
  'Hutchinson County',
  'Buffalo County',
  'Dewey County',
  'Hughes County',
  'Sanborn County',
  'Hand County',
  'Yankton County',
  'Beadle County',
  'Davison County',
  'Jerauld County',
  'Stanley County',
  'Potter County',
  'Charles Mix County',
  'Marshall County',
  'Moody County',
  'Todd County',
  'Lyman County',
  'Spink County',
  'Brookings County',
  'Hamlin County'],
 'Tennessee': ['Maury County',
  'Union County',
  'Montgomery County',
  'Dickson County',
  'Morgan County',
  'Grundy County',
  'Monroe County',
  'Henry County',
  'Cocke County',
  'Crockett County',
  'DeKalb County',
  'Lake County',
  'Knox County',
  'Lewis County',
  'McMinn County',
  'Marshall County',
  'Obion County',
  'Rhea County',
  'Scott County',
  'Tipton County',
  'Anderson County',
  'Dyer County',
  'Fentress County',
  'Gibson County',
  'Hamilton County',
  'Loudon County',
  'Rutherford County',
  'Smith County',
  'Wilson County',
  'Sullivan County',
  'Warren County',
  'Washington County',
  'Benton County',
  'Campbell County',
  'Cannon County',
  'Fayette County',
  'Hancock County',
  'Johnson County',
  'Lincoln County',
  'Moore County',
  'Franklin County',
  'Blount County',
  'Lawrence County',
  'Carter County',
  'Grainger County',
  'Lauderdale County',
  'Marion County',
  'Overton County',
  'Sumner County',
  'Trousdale County',
  'Williamson County',
  'Clay County',
  'Greene County',
  'Shelby County',
  'Van Buren County',
  'Henderson County',
  'Hickman County',
  'Jefferson County',
  'Sequatchie County',
  'Sevier County',
  'Carroll County',
  'Chester County',
  'Davidson County',
  'Jackson County',
  'Perry County',
  'Roane County',
  'Meigs County',
  'Hamblen County',
  'Haywood County',
  'Houston County',
  'Hardin County',
  'Hardeman County',
  'Polk County',
  'White County',
  'Unicoi County',
  'Weakley County',
  'Bledsoe County',
  'Coffee County',
  'Hawkins County',
  'Macon County',
  'Robertson County',
  'Cheatham County',
  'Giles County',
  'Madison County',
  'Pickett County',
  'Wayne County',
  'Bedford County',
  'Cumberland County',
  'Claiborne County',
  'Humphreys County',
  'Putnam County',
  'Stewart County',
  'Decatur County',
  'McNairy County',
  'Bradley County'],
 'Iowa': ['Cass County',
  'Cherokee County',
  'Crawford County',
  'Des Moines County',
  'Fayette County',
  'Harrison County',
  'Kossuth County',
  'Mills County',
  'Monona County',
  'Muscatine County',
  'Osceola County',
  'Polk County',
  'Webster County',
  'Story County',
  'Woodbury County',
  'Black Hawk County',
  'Grundy County',
  'Jackson County',
  'Jones County',
  'Lee County',
  'Mitchell County',
  'Warren County',
  'Sac County',
  'Plymouth County',
  'Clay County',
  'Clinton County',
  'Delaware County',
  'Wayne County',
  'Linn County',
  'Scott County',
  "O'Brien County",
  'Benton County',
  'Dubuque County',
  'Hamilton County',
  'Pocahontas County',
  'Union County',
  'Van Buren County',
  'Ringgold County',
  'Davis County',
  'Adair County',
  'Audubon County',
  'Clarke County',
  'Ida County',
  'Keokuk County',
  'Monroe County',
  'Wapello County',
  'Sioux County',
  'Calhoun County',
  'Cedar County',
  'Cerro Gordo County',
  'Greene County',
  'Hardin County',
  'Lucas County',
  'Winnebago County',
  'Palo Alto County',
  'Appanoose County',
  'Iowa County',
  'Jasper County',
  'Winneshiek County',
  'Poweshiek County',
  'Marshall County',
  'Boone County',
  'Bremer County',
  'Howard County',
  'Emmet County',
  'Hancock County',
  'Madison County',
  'Marion County',
  'Wright County',
  'Montgomery County',
  'Mahaska County',
  'Buchanan County',
  'Decatur County',
  'Jefferson County',
  'Allamakee County',
  'Dallas County',
  'Butler County',
  'Fremont County',
  'Taylor County',
  'Worth County',
  'Adams County',
  'Chickasaw County',
  'Dickinson County',
  'Johnson County',
  'Tama County',
  'Franklin County',
  'Carroll County',
  'Floyd County',
  'Louisa County',
  'Lyon County',
  'Shelby County',
  'Henry County',
  'Page County',
  'Pottawattamie County',
  'Clayton County',
  'Buena Vista County',
  'Guthrie County',
  'Humboldt County',
  'Washington County'],
 'Kansas': ['Smith County',
  'Grant County',
  'Kingman County',
  'Butler County',
  'Nemaha County',
  'Pottawatomie County',
  'Cherokee County',
  'Lincoln County',
  'Sumner County',
  'Trego County',
  'Wilson County',
  'Woodson County',
  'Ness County',
  'Osborne County',
  'Bourbon County',
  'Hamilton County',
  'Kiowa County',
  'Shawnee County',
  'Sherman County',
  'Thomas County',
  'Montgomery County',
  'Morris County',
  'Rawlins County',
  'Rooks County',
  'Clark County',
  'Ellsworth County',
  'Harper County',
  'Russell County',
  'Lyon County',
  'Pawnee County',
  'Allen County',
  'Comanche County',
  'Elk County',
  'Gove County',
  'Harvey County',
  'Hodgeman County',
  'Kearny County',
  'Stafford County',
  'McPherson County',
  'Osage County',
  'Greeley County',
  'Coffey County',
  'Crawford County',
  'Ellis County',
  'Greenwood County',
  'Labette County',
  'Linn County',
  'Sedgwick County',
  'Seward County',
  'Republic County',
  'Graham County',
  'Johnson County',
  'Douglas County',
  'Sheridan County',
  'Miami County',
  'Gray County',
  'Wallace County',
  'Stevens County',
  'Washington County',
  'Chautauqua County',
  'Morton County',
  'Reno County',
  'Cloud County',
  'Scott County',
  'Doniphan County',
  'Haskell County',
  'Lane County',
  'Neosho County',
  'Brown County',
  'Phillips County',
  'Riley County',
  'Decatur County',
  'Jefferson County',
  'Jackson County',
  'Logan County',
  'Wyandotte County',
  'Clay County',
  'Saline County',
  'Wabaunsee County',
  'Mitchell County',
  'Atchison County',
  'Finney County',
  'Leavenworth County',
  'Stanton County',
  'Meade County',
  'Pratt County',
  'Anderson County',
  'Geary County',
  'Ford County',
  'Marshall County',
  'Cheyenne County',
  'Cowley County',
  'Franklin County',
  'Jewell County',
  'Rice County',
  'Chase County',
  'Wichita County',
  'Norton County',
  'Barton County',
  'Edwards County',
  'Rush County',
  'Marion County',
  'Ottawa County',
  'Barber County',
  'Dickinson County'],
 'Kentucky': ['Butler County',
  'Edmonson County',
  'Harrison County',
  'Bracken County',
  'Lyon County',
  'Elliott County',
  'Jefferson County',
  'Larue County',
  'Mason County',
  'Mercer County',
  'Robertson County',
  'Russell County',
  'Washington County',
  'Ballard County',
  'Barren County',
  'Green County',
  'Hancock County',
  'Martin County',
  'Hardin County',
  'McLean County',
  'Ohio County',
  'Powell County',
  'Webster County',
  'Caldwell County',
  'Casey County',
  'Christian County',
  'Grayson County',
  'Henry County',
  'Hopkins County',
  'Jackson County',
  'Laurel County',
  'Marshall County',
  'Meade County',
  'Montgomery County',
  'Nicholas County',
  'Oldham County',
  'Owen County',
  'Rockcastle County',
  'Scott County',
  'Warren County',
  'Allen County',
  'Bourbon County',
  'Boyd County',
  'Bullitt County',
  'Crittenden County',
  'Fayette County',
  'Fulton County',
  'Johnson County',
  'Menifee County',
  'Clay County',
  'Morgan County',
  'Perry County',
  'Wolfe County',
  'Bell County',
  'Breathitt County',
  'Graves County',
  'Hart County',
  'Wayne County',
  'Marion County',
  'Trigg County',
  'Boone County',
  'Leslie County',
  'Knox County',
  'Lawrence County',
  'Livingston County',
  'Pike County',
  'Shelby County',
  'Anderson County',
  'Breckinridge County',
  'Franklin County',
  'Kenton County',
  'Madison County',
  'Magoffin County',
  'Owsley County',
  'Simpson County',
  'Taylor County',
  'Todd County',
  'Carlisle County',
  'Clinton County',
  'Gallatin County',
  'Garrard County',
  'Fleming County',
  'Campbell County',
  'Trimble County',
  'Hickman County',
  'Nelson County',
  'Grant County',
  'Logan County',
  'Pendleton County',
  'Spencer County',
  'Bath County',
  'Boyle County',
  'Harlan County',
  'Lincoln County',
  'Monroe County',
  'Union County',
  'Calloway County',
  'Daviess County',
  'Pulaski County',
  'Henderson County',
  'Knott County',
  'Muhlenberg County',
  'Adair County',
  'Cumberland County',
  'Lee County',
  'Lewis County',
  'Woodford County',
  'Jessamine County',
  'Letcher County',
  'McCracken County',
  'Whitley County',
  'Floyd County',
  'McCreary County',
  'Metcalfe County',
  'Rowan County',
  'Clark County',
  'Carroll County',
  'Estill County',
  'Greenup County',
  'Carter County'],
 'Louisiana': ['Vermilion Parish',
  'St. Charles Parish',
  'Concordia Parish',
  'Tensas Parish',
  'St. James Parish',
  'Grant Parish',
  'Jefferson Parish',
  'Bienville Parish',
  'Bossier Parish',
  'Cameron Parish',
  'East Feliciana Parish',
  'St. John the Baptist Parish',
  'Plaquemines Parish',
  'Ouachita Parish',
  'Rapides Parish',
  'Washington Parish',
  'St. Landry Parish',
  'Tangipahoa Parish',
  'Acadia Parish',
  'St. Mary Parish',
  'West Carroll Parish',
  'St. Tammany Parish',
  'Union Parish',
  'Caldwell Parish',
  'Lafayette Parish',
  'Caddo Parish',
  'East Carroll Parish',
  'Ascension Parish',
  'Iberia Parish',
  'St. Bernard Parish',
  'St. Helena Parish',
  'West Baton Rouge Parish',
  'De Soto Parish',
  'Red River Parish',
  'Livingston Parish',
  'Natchitoches Parish',
  'Orleans Parish',
  'Catahoula Parish',
  'Calcasieu Parish',
  'Franklin Parish',
  'Assumption Parish',
  'Jackson Parish',
  'Richland Parish',
  'St. Martin Parish',
  'Winn Parish',
  'East Baton Rouge Parish',
  'Allen Parish',
  'Madison Parish',
  'Lafourche Parish',
  'Jefferson Davis Parish',
  'West Feliciana Parish',
  'Beauregard Parish',
  'Evangeline Parish',
  'Lincoln Parish',
  'Webster Parish',
  'Iberville Parish',
  'Morehouse Parish',
  'Terrebonne Parish',
  'Claiborne Parish',
  'Avoyelles Parish',
  'Pointe Coupee Parish',
  'Vernon Parish',
  'Sabine Parish',
  'LaSalle Parish'],
 'Maine': ['Oxford County',
  'Waldo County',
  'Penobscot County',
  'Androscoggin County',
  'Aroostook County',
  'Cumberland County',
  'Knox County',
  'York County',
  'Franklin County',
  'Somerset County',
  'Lincoln County',
  'Piscataquis County',
  'Washington County',
  'Sagadahoc County',
  'Kennebec County',
  'Hancock County'],
 'Maryland': ['Worcester County',
  'Baltimore city',
  'Talbot County',
  'Harford County',
  'Howard County',
  'Anne Arundel County',
  'Baltimore County',
  'Calvert County',
  'Garrett County',
  'Montgomery County',
  'Carroll County',
  "Queen Anne's County",
  "St. Mary's County",
  'Charles County',
  'Dorchester County',
  'Washington County',
  'Wicomico County',
  'Cecil County',
  'Caroline County',
  'Somerset County',
  'Allegany County',
  "Prince George's County",
  'Frederick County',
  'Kent County'],
 'Massachusetts': ['Suffolk County',
  'Barnstable County',
  'Dukes County',
  'Middlesex County',
  'Berkshire County',
  'Essex County',
  'Bristol County',
  'Hampden County',
  'Plymouth County',
  'Franklin County',
  'Norfolk County',
  'Hampshire County',
  'Nantucket County',
  'Worcester County'],
 'Michigan': ['Monroe County',
  'Allegan County',
  'Hillsdale County',
  'Alger County',
  'Oceana County',
  'Leelanau County',
  'Clare County',
  'Keweenaw County',
  'Isabella County',
  'Ottawa County',
  'Tuscola County',
  'Alpena County',
  'Ionia County',
  'Midland County',
  'Berrien County',
  'Oscoda County',
  'Crawford County',
  'Clinton County',
  'Gratiot County',
  'Huron County',
  'Lenawee County',
  'Mason County',
  'Montcalm County',
  'St. Joseph County',
  'St. Clair County',
  'Washtenaw County',
  'Arenac County',
  'Cass County',
  'Iron County',
  'Roscommon County',
  'Wayne County',
  'Branch County',
  'Jackson County',
  'Mackinac County',
  'Antrim County',
  'Houghton County',
  'Iosco County',
  'Lake County',
  'Montmorency County',
  'Presque Isle County',
  'Kalamazoo County',
  'Mecosta County',
  'Marquette County',
  'Newaygo County',
  'Osceola County',
  'Otsego County',
  'Calhoun County',
  'Cheboygan County',
  'Luce County',
  'Kent County',
  'Macomb County',
  'Bay County',
  'Saginaw County',
  'Shiawassee County',
  'Baraga County',
  'Charlevoix County',
  'Eaton County',
  'Delta County',
  'Gogebic County',
  'Emmet County',
  'Chippewa County',
  'Oakland County',
  'Muskegon County',
  'Lapeer County',
  'Sanilac County',
  'Ontonagon County',
  'Alcona County',
  'Kalkaska County',
  'Ingham County',
  'Ogemaw County',
  'Wexford County',
  'Dickinson County',
  'Menominee County',
  'Missaukee County',
  'Van Buren County',
  'Barry County',
  'Benzie County',
  'Schoolcraft County',
  'Grand Traverse County',
  'Genesee County',
  'Livingston County',
  'Manistee County',
  'Gladwin County'],
 'California': ['Lake County',
  'Mariposa County',
  'Yuba County',
  'Contra Costa County',
  'Lassen County',
  'Santa Barbara County',
  'Sonoma County',
  'Imperial County',
  'Mono County',
  'Alameda County',
  'Sacramento County',
  'Napa County',
  'Monterey County',
  'Sierra County',
  'San Diego County',
  'Yolo County',
  'Humboldt County',
  'Alpine County',
  'Mendocino County',
  'Santa Cruz County',
  'Los Angeles County',
  'Riverside County',
  'Santa Clara County',
  'Marin County',
  'Siskiyou County',
  'Shasta County',
  'Del Norte County',
  'San Luis Obispo County',
  'Glenn County',
  'Butte County',
  'Plumas County',
  'Kern County',
  'Orange County',
  'Calaveras County',
  'Sutter County',
  'San Mateo County',
  'Tuolumne County',
  'San Joaquin County',
  'Amador County',
  'Merced County',
  'Modoc County',
  'Inyo County',
  'Stanislaus County',
  'Tehama County',
  'San Benito County',
  'El Dorado County',
  'San Francisco County',
  'Tulare County',
  'Nevada County',
  'Madera County',
  'Trinity County',
  'San Bernardino County',
  'Placer County',
  'Solano County',
  'Colusa County',
  'Kings County',
  'Fresno County',
  'Ventura County'],
 'Colorado': ['Phillips County',
  'Archuleta County',
  'Denver County',
  'Kiowa County',
  'Huerfano County',
  'Baca County',
  'Chaffee County',
  'Gilpin County',
  'Kit Carson County',
  'Garfield County',
  'Gunnison County',
  'Jefferson County',
  'Mineral County',
  'Ouray County',
  'Rio Blanco County',
  'Sedgwick County',
  'Conejos County',
  'Costilla County',
  'Adams County',
  'Eagle County',
  'Lake County',
  'Moffat County',
  'Pitkin County',
  'Cheyenne County',
  'Crowley County',
  'Dolores County',
  'Jackson County',
  'Larimer County',
  'Montezuma County',
  'San Miguel County',
  'Boulder County',
  'Las Animas County',
  'Yuma County',
  'Routt County',
  'Summit County',
  'Clear Creek County',
  'Delta County',
  'Pueblo County',
  'Morgan County',
  'Park County',
  'Mesa County',
  'Prowers County',
  'El Paso County',
  'Washington County',
  'Arapahoe County',
  'Broomfield County',
  'Weld County',
  'Custer County',
  'Douglas County',
  'La Plata County',
  'Rio Grande County',
  'Bent County',
  'San Juan County',
  'Logan County',
  'Teller County',
  'Elbert County',
  'Lincoln County',
  'Alamosa County',
  'Fremont County',
  'Montrose County',
  'Saguache County',
  'Hinsdale County',
  'Grand County',
  'Otero County'],
 'Connecticut': ['New Haven County',
  'Tolland County',
  'Hartford County',
  'Windham County',
  'Middlesex County',
  'Litchfield County',
  'New London County',
  'Fairfield County'],
 'Delaware': ['New Castle County', 'Sussex County', 'Kent County'],
 'District of Columbia': ['District of Columbia'],
 'Florida': ['Okaloosa County',
  'Taylor County',
  'Washington County',
  'Duval County',
  'Bradford County',
  'Brevard County',
  'Clay County',
  'Lafayette County',
  'Lake County',
  'Nassau County',
  'Pinellas County',
  'Polk County',
  'St. Lucie County',
  'Glades County',
  'Hendry County',
  'Indian River County',
  'Jackson County',
  'Palm Beach County',
  'St. Johns County',
  'Seminole County',
  'Miami-Dade County',
  'Bay County',
  'Flagler County',
  'Franklin County',
  'Hamilton County',
  'Liberty County',
  'Sumter County',
  'Gadsden County',
  'Holmes County',
  'Lee County',
  'Marion County',
  'Collier County',
  'Orange County',
  'Pasco County',
  'Highlands County',
  'Suwannee County',
  'DeSoto County',
  'Calhoun County',
  'Columbia County',
  'Dixie County',
  'Putnam County',
  'Union County',
  'Manatee County',
  'Levy County',
  'Baker County',
  'Volusia County',
  'Leon County',
  'Madison County',
  'Escambia County',
  'Hernando County',
  'Wakulla County',
  'Hillsborough County',
  'Gulf County',
  'Osceola County',
  'Walton County',
  'Jefferson County',
  'Hardee County',
  'Okeechobee County',
  'Gilchrist County',
  'Alachua County',
  'Charlotte County',
  'Martin County',
  'Sarasota County',
  'Citrus County',
  'Santa Rosa County',
  'Broward County',
  'Monroe County'],
 'Georgia': ['Calhoun County',
  'Macon County',
  'Bleckley County',
  'Bibb County',
  'Marion County',
  'Schley County',
  'Dooly County',
  'Franklin County',
  'Effingham County',
  'Lamar County',
  'Emanuel County',
  'Quitman County',
  'Jasper County',
  'Johnson County',
  'Liberty County',
  'Mitchell County',
  'Seminole County',
  'Tift County',
  'Twiggs County',
  'Polk County',
  'Talbot County',
  'Taylor County',
  'Terrell County',
  'Thomas County',
  'Toombs County',
  'Wilkinson County',
  'Ben Hill County',
  'Burke County',
  'Catoosa County',
  'Chattahoochee County',
  'Chattooga County',
  'Columbia County',
  'Decatur County',
  'Floyd County',
  'Forsyth County',
  'Habersham County',
  'Lowndes County',
  'Meriwether County',
  'Monroe County',
  'Sumter County',
  'Taliaferro County',
  'Baker County',
  'Butts County',
  'Candler County',
  'Carroll County',
  'Crawford County',
  'Crisp County',
  'Coweta County',
  'Cobb County',
  'Dade County',
  'Walton County',
  'Brooks County',
  'Dodge County',
  'Elbert County',
  'Fayette County',
  'Jenkins County',
  'Newton County',
  'Pickens County',
  'Colquitt County',
  'Dawson County',
  'Clayton County',
  'Hall County',
  'Heard County',
  'Hancock County',
  'McDuffie County',
  'Morgan County',
  'Dougherty County',
  'Fannin County',
  'Houston County',
  'Laurens County',
  'Spalding County',
  'Telfair County',
  'Union County',
  'Washington County',
  'White County',
  'Paulding County',
  'Pike County',
  'Richmond County',
  'Tattnall County',
  'Berrien County',
  'Walker County',
  'Gwinnett County',
  'Barrow County',
  'Charlton County',
  'Clinch County',
  'Bartow County',
  'Douglas County',
  'Grady County',
  'Jeff Davis County',
  'Montgomery County',
  'Oglethorpe County',
  'Randolph County',
  'Rockdale County',
  'Ware County',
  'Wayne County',
  'Wheeler County',
  'Wilcox County',
  'Baldwin County',
  'Bulloch County',
  'Clarke County',
  'Echols County',
  'Glynn County',
  'Haralson County',
  'Jefferson County',
  'Jones County',
  'Murray County',
  'Muscogee County',
  'Rabun County',
  'Stewart County',
  'Treutlen County',
  'Irwin County',
  'Atkinson County',
  'Bacon County',
  'Brantley County',
  'Whitfield County',
  'Troup County',
  'Harris County',
  'Worth County',
  'Evans County',
  'Webster County',
  'Glascock County',
  'Chatham County',
  'Lanier County',
  'Madison County',
  'Hart County',
  'McIntosh County',
  'Putnam County',
  'Warren County',
  'Bryan County',
  'Camden County',
  'Early County',
  'Coffee County',
  'Gilmer County',
  'Wilkes County',
  'Gordon County',
  'Cherokee County',
  'Lee County',
  'Greene County',
  'Cook County',
  'Fulton County',
  'Lumpkin County',
  'Miller County',
  'Oconee County',
  'Henry County',
  'Long County',
  'Stephens County',
  'Upson County',
  'Peach County',
  'Pierce County',
  'Screven County',
  'Banks County',
  'Clay County',
  'DeKalb County',
  'Jackson County',
  'Lincoln County',
  'Appling County',
  'Pulaski County',
  'Towns County',
  'Turner County'],
 'Idaho': ['Washington County',
  'Cassia County',
  'Gem County',
  'Valley County',
  'Adams County',
  'Nez Perce County',
  'Kootenai County',
  'Lewis County',
  'Butte County',
  'Twin Falls County',
  'Owyhee County',
  'Boise County',
  'Caribou County',
  'Ada County',
  'Bannock County',
  'Bingham County',
  'Camas County',
  'Canyon County',
  'Jefferson County',
  'Latah County',
  'Payette County',
  'Benewah County',
  'Clark County',
  'Elmore County',
  'Fremont County',
  'Shoshone County',
  'Idaho County',
  'Power County',
  'Oneida County',
  'Lincoln County',
  'Franklin County',
  'Jerome County',
  'Minidoka County',
  'Blaine County',
  'Boundary County',
  'Gooding County',
  'Bear Lake County',
  'Bonneville County',
  'Clearwater County',
  'Lemhi County',
  'Bonner County',
  'Custer County',
  'Madison County',
  'Teton County'],
 'Hawaii': ['Hawaii County',
  'Maui County',
  'Kauai County',
  'Kalawao County',
  'Honolulu County'],
 'Illinois': ['Jersey County',
  'Putnam County',
  'De Witt County',
  'Fayette County',
  'Lee County',
  'Logan County',
  'Macoupin County',
  'Richland County',
  'Saline County',
  'Washington County',
  'Montgomery County',
  'Whiteside County',
  'Adams County',
  'Clinton County',
  'DeKalb County',
  'Edwards County',
  'Jasper County',
  'Jefferson County',
  'Will County',
  'Williamson County',
  'Douglas County',
  'Fulton County',
  'Greene County',
  'Hardin County',
  'Henry County',
  'Knox County',
  'Lake County',
  'Massac County',
  'Scott County',
  'Cass County',
  'LaSalle County',
  'Hancock County',
  'Grundy County',
  'Kankakee County',
  'DuPage County',
  'Sangamon County',
  'Menard County',
  'Stephenson County',
  'Cook County',
  'Ogle County',
  'Morgan County',
  'White County',
  'Woodford County',
  'Henderson County',
  'McHenry County',
  'McLean County',
  'Perry County',
  'Pike County',
  'Rock Island County',
  'St. Clair County',
  'Wabash County',
  'Calhoun County',
  'Cumberland County',
  'Jo Daviess County',
  'Kane County',
  'Lawrence County',
  'Brown County',
  'Marshall County',
  'Iroquois County',
  'Christian County',
  'Clay County',
  'Gallatin County',
  'Jackson County',
  'Monroe County',
  'Peoria County',
  'Union County',
  'Winnebago County',
  'Piatt County',
  'Pulaski County',
  'Schuyler County',
  'Stark County',
  'Edgar County',
  'Bond County',
  'Boone County',
  'Bureau County',
  'Carroll County',
  'Coles County',
  'Crawford County',
  'Vermilion County',
  'Clark County',
  'Effingham County',
  'Hamilton County',
  'Johnson County',
  'Livingston County',
  'Tazewell County',
  'Warren County',
  'Madison County',
  'Mercer County',
  'Alexander County',
  'Randolph County',
  'Macon County',
  'Wayne County',
  'Franklin County',
  'McDonough County',
  'Moultrie County',
  'Pope County',
  'Shelby County',
  'Champaign County',
  'Ford County',
  'Kendall County',
  'Marion County',
  'Mason County'],
 'Indiana': ['Monroe County',
  'Fountain County',
  'Elkhart County',
  'Crawford County',
  'Cass County',
  'Marion County',
  'Clay County',
  'Hendricks County',
  'Franklin County',
  'Grant County',
  'Jackson County',
  'Howard County',
  'Owen County',
  'Randolph County',
  'Whitley County',
  'Brown County',
  'Clinton County',
  'Union County',
  'Lawrence County',
  'Daviess County',
  'Dearborn County',
  'Knox County',
  'Perry County',
  'Pulaski County',
  'Posey County',
  'Warren County',
  'Vermillion County',
  'Allen County',
  'Decatur County',
  'Floyd County',
  'Jennings County',
  'Johnson County',
  'Morgan County',
  'Gibson County',
  'Orange County',
  'Kosciusko County',
  'Marshall County',
  'Vanderburgh County',
  'Blackford County',
  'Scott County',
  'Harrison County',
  'LaPorte County',
  'Wabash County',
  'Jasper County',
  'Martin County',
  'Porter County',
  'Shelby County',
  'Ripley County',
  'Spencer County',
  'Sullivan County',
  'Tipton County',
  'Tippecanoe County',
  'Vigo County',
  'Warrick County',
  'Hamilton County',
  'DeKalb County',
  'LaGrange County',
  'Bartholomew County',
  'Rush County',
  'Boone County',
  'Fulton County',
  'Lake County',
  'Montgomery County',
  'Noble County',
  'Adams County',
  'Fayette County',
  'Starke County',
  'Greene County',
  'Wayne County',
  'Dubois County',
  'Hancock County',
  'Ohio County',
  'Parke County',
  'Benton County',
  'Putnam County',
  'Washington County',
  'Henry County',
  'Madison County',
  'Pike County',
  'Steuben County',
  'Miami County',
  'Wells County',
  'Delaware County',
  'Jefferson County',
  'Newton County',
  'St. Joseph County',
  'Switzerland County',
  'Carroll County',
  'Huntington County',
  'White County',
  'Jay County',
  'Clark County']}

@app.route('/')
# @app.route('/main')
def main():
    user = { 'nickname': 'COSMOS' } # fake user
    return render_template('main.html',
                            user = { 'nickname': 'COSMOS' },
                            title = 'Home'
                            )

@app.route('/index')
def index():
	return render_template("index.html",
       title = 'Index')

@app.route('/schools')
def schools():
	return render_template("schools.html",
       title = 'Schools')

@app.route('/businesses')
def businesses():
	return render_template("businesses.html",
       title = 'Businesses')


@app.route('/input',methods=['GET', 'POST'])
@app.route('/input/output',methods=['GET', 'POST'])
def input():
    form1 = InputForm(request.form)
    al_counties = counties_dict.get('Alabama')
    al_counties.sort()
    form1.counties.choices = al_counties
    if request.method == 'POST':
        state_selected = form1.state.data
        county_selected_1 = form1.counties.data
        county_selected_1=county_selected_1.replace("+"," ")
        county_selected = county_selected_1
        # return(county_selected_1)
        # if 'County' in county_selected_1:
        #     county_selected = county_selected_1
        # else:
        #     county_selected = county_selected_1+' County'
        # return (county_selected)

        output_list,figure = key_contact_individuals(state_selected,county_selected)
        total_population = output_list[0]
        key_contacts_5_17_L1= output_list[1]
        key_contacts_18_64_L1= output_list[2]
        key_contacts_H1= output_list[3]
        key_contacts_H2= output_list[4]
        sum_key_contact = float(key_contacts_5_17_L1)+float(key_contacts_18_64_L1)+float(key_contacts_H1)+float(key_contacts_H2)
        percent_key_pop = np.round((sum_key_contact/float(total_population))*100,2)
        # fig_script, fig_div = components(figure)
        return render_template("state_description.html"
                                ,fig=figure
                                ,state=state_selected
                                ,county = county_selected
                                ,population_str = "{:,}".format(total_population)
                                ,population=total_population
                                ,key_contacts_5_17_L1 = "{:,}".format(int(key_contacts_5_17_L1))
                                ,key_contacts_18_64_L1="{:,}".format(int(key_contacts_18_64_L1))
                                ,key_contacts_H1="{:,}".format(int(key_contacts_H1))
                                ,key_contacts_H2="{:,}".format(int(key_contacts_H2))
                                ,sum_key_contact="{:,}".format(int(sum_key_contact))
                                ,percent_key_pop=percent_key_pop
                                ,title = 'Data')
    else:
        flash('Please enter a valid value', 'danger')
        return render_template("input.html", form=form1
                                ,title = 'Input')



@app.route('/input/input_parameters/',methods=['GET', 'POST'])
@app.route('/input/results/',methods=['GET', 'POST'])
def input_fatalities():
    state_selected = request.args.get('state_selected')
    county_selected = request.args.get('county_selected')
    total_population = request.args.get('population')
    population_str= request.args.get('population_str')
    key_contacts_5_17_L1 = request.args.get('key_contacts_5_17_L1')
    key_contacts_18_64_L1 = request.args.get('key_contacts_18_64_L1')
    key_contacts_H1 = request.args.get('key_contacts_H1')
    key_contacts_H2 = request.args.get('key_contacts_H2')
    num_fatalities_daily= request.args.get('num_fatalities_daily')
    arg_1 = request.args.get('arg1')
    arg_2 = request.args.get('arg2')
    form = InputForm(request.form)


    if request.method == 'POST':
        if arg_1=='output':
            num_cases_3_weeks = form.num_cases_3_weeks.data
            num_kits_calc= form.num_kits.data
            num_masks_calc= form.num_masks.data
            num_fatalities_7=form.num_fatalities_7.data
            num_days=form.num_days.data
            county_selected = request.args.get('county_selected')
            fraction_positive_comply_quarantine = 0.85
            fraction_contagious_day = float(num_cases_3_weeks)*((1-(fraction_positive_comply_quarantine))+4)/float(total_population)
            COVID_19_testing_kits_available = float(num_kits_calc)*float(total_population)/1000
            N95_masks_available = float(num_masks_calc)*float(total_population)/1000
            avg_daily_fatalities = round((float(num_fatalities_7)/float(num_days)),3)

            list_census_data=[float(total_population),float(key_contacts_5_17_L1),float(key_contacts_18_64_L1),float(key_contacts_H1),float(key_contacts_H2)]
            LP_Input = LP_input_function(list_census_data,fraction_contagious_day,COVID_19_testing_kits_available,N95_masks_available)
            #Run for normalcy 0
            normalcy = 0
            #Corresponding Scenario parameter needs to be passed to LP function. Scenario 1 corresponds to Normalcy 0
            #Scenario 10 corresponds to Normalcy 9
            Scenario = "Scenario" + str(normalcy+1)

            TotalPopulation=float(total_population)
            Normalcy_Score,obj_val,obj_coeff,LP_decision = LP(LP_Input,Scenario)
            min_activity = LP_Input.query('Parameter1=="min all"')['Scenario1']
            max_activity = LP_Input.query('Parameter1=="max all"')['Scenario1']
            minimum_normalcy = 10*(Normalcy_Score[0]-min_activity[0])/(max_activity[0]-min_activity[0])
            if obj_val is None:
                obj_val=0
            else:
                obj_val = obj_val
            obj_dict = {round(minimum_normalcy,2):obj_val}
            
            fig_div = dashboard_plots(LP_decision,obj_val,TotalPopulation,county_selected,minimum_normalcy)
            figure_dict = {round(minimum_normalcy,2):fig_div}
            scenario_start = math.ceil(minimum_normalcy)
            for i in range(scenario_start,10):
                Scenario_LP = "Scenario" + str(i+1)
                obj_val_i,obj_coeff_i,LP_decision_i = LP(LP_Input,Scenario_LP)
                if obj_val_i is None:
                    obj_val_i=0
                else:
                    obj_val_i = obj_val_i
                obj_dict[i] = obj_val_i
                # fig_div_i = dashboard_plots(LP_decision_i,obj_val_i,TotalPopulation,county_selected,i)
                # figure_dict[i] = fig_div_i
             #Print the table for normalcy values

            list_normalcy = list(obj_dict.keys())
            list_obj_values = list(obj_dict.values())
            min_obj_key = list_normalcy[0]
            max_obj_key = list_normalcy[-1]
            min_obj_values = round(obj_dict.get(min_obj_key),3)
            max_obj_values = round(obj_dict.get(max_obj_key),3)
            list_first_column = [round(x * (5.15/4.15),3) for x in list_obj_values]
            list_second_column = [round(x ,3) for x in list_obj_values]
            list_third_column = [round(x * (3.15/4.15),3) for x in list_obj_values]
            list_fourth_column = [round(x * (2.15/4.15),3) for x in list_obj_values]
            list_fifth_column = [round(x * (1.15/4.15),3) for x in list_obj_values]

            fig_obj = make_subplots(rows=2, cols=1,vertical_spacing =0.0001,row_heights = [0.09,0.95],
                        specs=[[{"type": "table"}],
                               [{"type": "table"}]])

            fig_obj.add_trace(go.Table(header=dict(values=['<b>Normalcy Scale 0-10</b>','<b>5:1</b>','<b>4:1</b>','<b>3:1</b>','<b>2:1</b>','<b>1:1</b>'],
                                                          line_color='darkslategray',fill_color = 'white',align=['left','center'],font=dict(family='Times New Roman',color='black', size=17),
                                                            height =30),
                                                cells=dict(values=[list_normalcy,list_first_column,list_second_column,list_third_column,
                                                                   list_fourth_column,list_fifth_column],
                                                                   line_color='darkslategray',
                                                           fill_color=['white','white','cyan','white','white','white'],align=['left', 'center'],
                                                           font=dict(family='Times New Roman',color='black', size=17),height =30)),row=2,col=1)


            fig_obj.add_trace(go.Table(header=dict(values=['<b>Ratio of Unknown to Known Cases</b>'],
                                                     line_color='darkslategray',
                            fill_color = ['white'],align=['center'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                                         row=1,col=1)


            fig_obj.update_layout(height=350,margin=dict(l=20,r=20,b=20,t=20))

            fig_obj_div = plotly.offline.plot(fig_obj, include_plotlyjs=False, output_type='div')
            output_choices = list(figure_dict.keys())
            form.normalcy_choices.choices=list_normalcy
            vals = list(figure_dict.values())
            list_LP_decision_values=vals[0]
            return render_template("output.html"
                                    ,title='Results'
                                    ,fig_1_div=fig_obj_div
                                    ,form= form
                                    ,min_obj_values=min_obj_values
                                    ,max_obj_values=max_obj_values
                                    ,min_obj_key=min_obj_key
                                    ,num_cases_3_weeks = num_cases_3_weeks
                                    ,COVID_19_testing_kits_available = int(COVID_19_testing_kits_available)
                                    ,N95_masks_available = int(N95_masks_available)
                                    ,num_fatalities_7=num_fatalities_7
                                    ,fraction_positive_comply_quarantine = 0.85
                                    ,fraction_contagious_day = fraction_contagious_day
                                    ,state_selected = state_selected
                                    ,county_selected = county_selected
                                    ,total_population = total_population
                                    ,key_contacts_5_17_L1 = key_contacts_5_17_L1
                                    ,key_contacts_18_64_L1 = key_contacts_18_64_L1
                                    ,key_contacts_H1 = key_contacts_H1
                                    ,key_contacts_H2 = key_contacts_H2
                                    ,avg_daily_fatalities= round(avg_daily_fatalities,3)
                                    )


        if arg_2=='more':
            norm = form.normalcy_choices.data
            state_selected = request.args.get('state')
            county_selected = request.args.get('county')
            total_population = request.args.get('total_population')
            key_contacts_5_17_L1 = request.args.get('key_contacts_5_17_L1')
            key_contacts_18_64_L1 = request.args.get('key_contacts_18_64_L1')
            key_contacts_H1 = request.args.get('key_contacts_H1')
            key_contacts_H2 = request.args.get('key_contacts_H2')
            fraction_contagious_day=request.args.get('fraction_contagious_day')
            COVID_19_testing_kits_available=request.args.get('COVID_19_testing_kits_available')
            N95_masks_available=request.args.get('N95_masks_available')
            # COVID_19_testing_kits_available=(float(num_kits_calc)*float(total_population))/1000
            # N95_masks_available=float(num_masks_calc)*float(total_population)/1000

            sum_key_contact = float(key_contacts_5_17_L1)+float(key_contacts_18_64_L1)+float(key_contacts_H1)+float(key_contacts_H2)
            percent_key_pop = np.round((sum_key_contact/float(total_population))*100,2)
            list_census_data=[float(total_population),float(key_contacts_5_17_L1),float(key_contacts_18_64_L1),float(key_contacts_H1),float(key_contacts_H2)]
            LP_Input = LP_input_function(list_census_data,fraction_contagious_day,COVID_19_testing_kits_available,N95_masks_available)
            # return str(COVID_19_testing_kits_available)
            #User enters normalcu
            normalcy = math.ceil(float(norm))
            #Corresponding Scenario parameter needs to be passed to LP function. Scenario 1 corresponds to Normalcy 0
            #Scenario 10 corresponds to Normalcy 9
            Scenario = "Scenario" + str(normalcy+1)
            # test_var=(LP_Input.query('Parameter1=="p" and Parameter2=="+"')[Scenario])
            obj_val,obj_coeff,LP_decision = LP(LP_Input,Scenario)
            if obj_val is None:
                obj_val=0
            else:
                obj_val=obj_val
            # return str(obj_val)
            figures_div = dashboard_plots(LP_decision,obj_val,float(total_population),county_selected,normalcy)

            # fig_test=request.args.get('list_LP_decision_values')
            # list_normalcy= request.args.get('list_normalcy')
            # # return list_normalcy
            # list_obj_values= request.args.get('list_obj_values')
            # list_LP_decision_values= request.args.get('list_LP_decision_values')
            # output_choices= request.args.get('output_choices')
            # normalcy_level = form_new.normalcy_choices.data
            # TotalPopulation=total_population
            # i=list_normalcy.index('9')
            # return normalcy_level
            # LP_decision_i = list_LP_decision_values[i]
            # obj_val_i = list_obj_values[i]
            # # obj_val_i = list_obj_values.index(normalcy_level)
            # figures_div = dashboard_plots(LP_decision_i,obj_val_i,TotalPopulation,county_selected,i)
            return render_template("extra_outputs.html"
                                    ,title='More Results'
                                    ,normalcy=normalcy
                                    ,state_selected=state_selected
                                    ,county_selected=county_selected
                                    # ,population_str = "{:,}".format(total_population)
                                    ,population=total_population
                                    ,key_contacts_5_17_L1 = "{:,}".format(int(float(key_contacts_5_17_L1)))
                                    ,key_contacts_18_64_L1="{:,}".format(int(float(key_contacts_18_64_L1)))
                                    ,key_contacts_H1="{:,}".format(int(float(key_contacts_H1)))
                                    ,key_contacts_H2="{:,}".format(int(float(key_contacts_H2)))
                                    ,sum_key_contact="{:,}".format(int(float(sum_key_contact)))
                                    ,percent_key_pop=percent_key_pop
                                    ,COVID_19_testing_kits_available=COVID_19_testing_kits_available
                                    ,N95_masks_available=N95_masks_available
                                    ,fig_2_div=figures_div[0]
                                    ,fig_3_div=figures_div[1]
                                    ,fig_4_div=figures_div[2]
                                    ,fig_5_div=figures_div[3]
                                    ,fig_6_div=figures_div[4]
                                    ,fig_7_div=figures_div[5]
                                    ,fig_8_div=figures_div[6]
                                    )

    else:
        return render_template("input_fatalities.html"
                                ,form=form
                                ,state_selected=state_selected
                                ,county_selected=county_selected
                                ,population_str = population_str
                                ,population = float(total_population.replace(',',''))
                                ,key_contacts_5_17_L1 = float(key_contacts_5_17_L1.replace(',',''))
                                ,key_contacts_18_64_L1=float(key_contacts_18_64_L1.replace(',',''))
                                ,key_contacts_H1=float(key_contacts_H1.replace(',',''))
                                ,key_contacts_H2=float(key_contacts_H2.replace(',',''))
                                ,num_fatalities_daily=0
                                ,fraction_positive_comply_quarantine = 0.85
                                ,fraction_unknown_cases = 0.8
                                ,fraction_contagious_day=0
                                ,number_contagious_day_5=0
                                , title = 'More Inputs')

@app.route('/c3ai')
# @app.route('/main')
def main_c3ai():
    return render_template('main_c3ai.html',
                            title = 'Home'
                            )

@app.route('/testing_popatrisk',methods=['GET', 'POST'])
@app.route('/testing_popatrisk/output',methods=['GET', 'POST'])
def testing_popatrisk():
    form1 = InputForm(request.form)
    al_counties = counties_dict.get('Alabama')
    al_counties.sort()
    form1.counties.choices = al_counties
    if request.method == 'POST':
        state_selected = form1.state.data
        county_selected_1 = form1.counties.data
        county_selected_1=county_selected_1.replace("+"," ")
        county_selected = county_selected_1
        # return(county_selected_1)
        # if 'County' in county_selected_1:
        #     county_selected = county_selected_1
        # else:
        #     county_selected = county_selected_1+' County'
        # return (county_selected)

        output_list,group_list,figure = key_contact_individuals_c3ai(state_selected,county_selected)
        total_population = output_list[0]
        key_contacts_5_17_L1= output_list[1]
        key_contacts_18_64_L1= output_list[2]
        key_contacts_H1= output_list[3]
        key_contacts_H2= output_list[4]
        
        number_sheltered_high_risk= group_list[0]
        key_contact_total= group_list[1]
        number_unrestricted_low_risk= group_list[2]
        
        sum_key_contact = float(key_contacts_5_17_L1)+float(key_contacts_18_64_L1)+float(key_contacts_H1)+float(key_contacts_H2)
        percent_key_pop = np.round((sum_key_contact/float(total_population))*100,2)
        
        percent_key_contact_total = np.round((key_contact_total/float(total_population))*100,2)
        percent_number_unrestricted_low_risk = np.round((number_unrestricted_low_risk/float(total_population))*100,2)
        percent_number_sheltered_high_risk = np.round((number_sheltered_high_risk/float(total_population))*100,2)
        
        # fig_script, fig_div = components(figure)
        return render_template("state_description_c3ai.html"
                                ,fig=figure
                                ,state=state_selected
                                ,county = county_selected
                                ,population_str = "{:,}".format(total_population)
                                ,population=total_population
                                ,key_contacts_5_17_L1 = "{:,}".format(int(key_contacts_5_17_L1))
                                ,key_contacts_18_64_L1="{:,}".format(int(key_contacts_18_64_L1))
                                ,key_contacts_H1="{:,}".format(int(key_contacts_H1))
                                ,key_contacts_H2="{:,}".format(int(key_contacts_H2))
                                ,sum_key_contact="{:,}".format(int(sum_key_contact))
                                ,percent_key_pop=percent_key_pop
                                , number_sheltered_high_risk=number_sheltered_high_risk
                                , key_contact_total=key_contact_total
                                , number_unrestricted_low_risk=number_unrestricted_low_risk
                                
                                ,number_sheltered_high_risk_str="{:,}".format(int(number_sheltered_high_risk))
                                ,key_contact_total_str="{:,}".format(int(key_contact_total))
                                ,number_unrestricted_low_risk_str="{:,}".format(int(number_unrestricted_low_risk))
                                
                                ,percent_key_contact_total = percent_key_contact_total
                                ,percent_number_unrestricted_low_risk = percent_number_unrestricted_low_risk
                                ,percent_number_sheltered_high_risk = percent_number_sheltered_high_risk
                                ,title = 'Data')
    else:
        flash('Please enter a valid value', 'danger')
        return render_template("input_popatrisk.html", form=form1
                                ,title = 'Input')


@app.route('/c3ai/input/input_parameters/',methods=['GET', 'POST'])
@app.route('/c3ai/input/results/',methods=['GET', 'POST'])
def input_fatalities_c3ai():
    state_selected = request.args.get('state_selected')
    county_selected = request.args.get('county_selected')
    total_population = request.args.get('population')
    key_contacts_5_17_L1 = request.args.get('key_contacts_5_17_L1')
    key_contacts_18_64_L1 = request.args.get('key_contacts_18_64_L1')
    key_contacts_H1 = request.args.get('key_contacts_H1')
    key_contacts_H2 = request.args.get('key_contacts_H2')
    num_fatalities_daily= request.args.get('num_fatalities_daily')
    number_sheltered_high_risk= request.args.get('number_sheltered_high_risk')
    key_contact_total= request.args.get('key_contact_total')
    percent_key_contact_total=request.args.get('percent_key_contact_total')
    number_unrestricted_low_risk= request.args.get('number_unrestricted_low_risk')
    arg_1 = request.args.get('arg1')
    arg_2 = request.args.get('arg2')
    arg_3 = request.args.get('arg_3')
    arg_4 = request.args.get('arg_4')
    route1 = request.args.get('route1')
    route2 = request.args.get('route2')
    route3 = request.args.get('route3')
    avg_daily_fatalities = request.args.get('avg_daily_fatalities')
    num_fatalities_7 = request.args.get('num_fatalities_7')
    num_days = request.args.get('num_days')
    num_cases_3_weeks = request.args.get('num_cases_3_weeks')
    form = InputForm(request.form)
    form_date = DateForm(request.form)
    if form_date.validate_on_submit():
        placeholder_value =1
        # continue
        # return 'Start Date is : {} End Date is : {}'.format(form_date.date_field_cases_start.data, form_date.date_field_cases_end.data)
    else:
        return('Enter a valid end date')
    county_init = county_selected
    county=county_init.replace('County','').replace(' ','')
    state_init=state_selected
    state=state_init.replace(' ','')
    id_county_state = county+'_'+state+'_'+'UnitedStates'

    # fatality plot section
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    fatalitycount = c3aidatalake.evalmetrics(
    "outbreaklocation",
    {
        "spec" : {
            "ids" : [id_county_state],
            "expressions" : ["JHU_ConfirmedDeaths"],
            "start" : '2020-04-01',
            "end" : today,
            "interval" : "DAY",
            }
        }
    )
    # colname = fatalitycount.columns[1]
    # data_fatality = [go.Bar(
    # x = fatalitycount.iloc[:,0],
    # y = fatalitycount[colname]
    # )]
    # fig_fatality = go.Figure(data=data_fatality)
    # fig_fatality_div = plotly.offline.plot(fig_fatality, include_plotlyjs=False, output_type='div')
    fatalitycount.columns = ['date','confirmed_fatalities','confirmed_fatalities_missing']
    fatalitycount['daily_fatalities']=fatalitycount.confirmed_fatalities.diff()
    fatalitycount.daily_fatalities.fillna(0,inplace=True)
    fatalitycount.daily_fatalities.replace(-1,0,inplace=True)
    fig_fatality = make_subplots(rows=1, cols=1,specs=[[{"type": "bar","rowspan": 1, "colspan": 1}]])

    fig_fatality.add_trace(go.Bar(x = fatalitycount.iloc[:,0],y = fatalitycount.daily_fatalities
                                    , textposition='inside', textfont_size=17))
    fig_fatality.update_layout(title_text="COVID-19 Fatalities by Day for {county_selected}, {state_selected}".format(county_selected=county_selected,state_selected=state_selected)
                                ,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},title_x=0.5)

    # fig_fatality.update_layout(height=350,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
    #                    margin=dict(l=20,r=20,b=20,t=20,pad=2))
    # iplot(fig_fatality)
    # fig_fatality.show()
    fig_fatality_div = plotly.offline.plot(fig_fatality, include_plotlyjs=False, output_type='div')


    # casecouts for three week data

    # today = pd.Timestamp.now().strftime("%Y-%m-%d")
    # delta= datetime.timedelta(days=21)
    # three_week_date=(pd.Timestamp.now()-delta).strftime("%Y-%m-%d")
    # this code pulls cases data till today
    casecounts = c3aidatalake.evalmetrics(
        "outbreaklocation",
        {
            "spec" : {
                "ids" : [id_county_state],
                "expressions" : ["JHU_ConfirmedCases"],
                "start" : '2020-04-01',
                "end" : today,
                "interval" : "DAY",
                    }
                }
            )
    colname = casecounts.columns[1]
    plotcasecount = casecounts.copy()

    #plot for number of cases
    # casecounts.columns = ['date','confirmed_cases','confirmed_cases_missing']
    casecounts.columns = ['date','confirmed_cases','confirmed_cases_missing']
    casecounts['daily_cases']=casecounts.confirmed_cases.diff()
    casecounts.daily_cases.fillna(0,inplace=True)
    casecounts.daily_cases.replace(-1,0,inplace=True)
    fig_cases = make_subplots(rows=1, cols=1,specs=[[{"type": "bar","rowspan": 1, "colspan": 1}]])

    fig_cases.add_trace(go.Bar(x = casecounts.iloc[:,0],y = casecounts.daily_cases
                                    , textposition='inside', textfont_size=17))
    fig_cases.update_layout(title_text="COVID-19 Cases by Day for {county_selected}, {state_selected}".format(county_selected=county_selected,state_selected=state_selected)
                                ,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},title_x=0.5)

    # fig_fatality.update_layout(height=350,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
    #                    margin=dict(l=20,r=20,b=20,t=20,pad=2))
    # iplot(fig_fatality)
    fig_cases_div = plotly.offline.plot(fig_cases, include_plotlyjs=False, output_type='div')

    # cases_from_api=(casecounts.iloc[-1,:][colname]-casecounts[casecounts.dates==three_week_date][colname][0])

    if arg_3=='fatalities':
        state_selected = request.args.get('state_selected')
        county_selected = request.args.get('county_selected')
        total_population = request.args.get('population')
        key_contacts_5_17_L1 = request.args.get('key_contacts_5_17_L1')
        key_contacts_18_64_L1 = request.args.get('key_contacts_18_64_L1')
        key_contacts_H1 = request.args.get('key_contacts_H1')
        key_contacts_H2 = request.args.get('key_contacts_H2')
        num_fatalities_daily= request.args.get('num_fatalities_daily')
        # num_cases_3_weeks = form.num_cases_3_weeks.data
        # num_cases_3_weeks=100
        # num_kits_calc= form.num_kits.data
        # num_masks_calc= form.num_masks.data
        # num_fatalities_7=form.num_fatalities_7.data
        # num_vaccines=form.num_vaccines.data
        # num_days=form.num_days.data
        start_date_fatalities = request.args.get('start_date')
        end_date_fatalities = request.args.get('end_date')
        number_sheltered_high_risk= request.args.get('number_sheltered_high_risk')
        key_contact_total= request.args.get('key_contact_total')
        percent_key_contact_total=request.args.get('percent_key_contact_total')
        # form_date.date_field_cases_start.data = pd.to_datetime(start_date_fatalities)
        # form_date.date_field_cases_end.data = pd.to_datetime(end_date_fatalities)
        # num_cases_3_weeks_date = form_date.num_cases_3_weeks_date.data
        # return('kits: ')

        #extract fatality count between the dates entered

        if pd.to_datetime(end_date_fatalities) == pd.to_datetime(start_date_fatalities):
            num_days = 1
            sub_fatality_count_data = fatalitycount[(pd.to_datetime(fatalitycount.date) >= pd.to_datetime(start_date_fatalities))]
            num_fatalities_7 = sub_fatality_count_data.daily_fatalities.sum()
        else:
            num_days_test = (pd.to_datetime(end_date_fatalities) - pd.to_datetime(start_date_fatalities))
            num_days = num_days_test.days
            sub_fatality_count_data = fatalitycount[(pd.to_datetime(fatalitycount.date) >= pd.to_datetime(start_date_fatalities)) & (pd.to_datetime(fatalitycount.date)<=pd.to_datetime(end_date_fatalities)) ]
            num_fatalities_7 = sub_fatality_count_data.daily_fatalities.sum()

        # county_selected = request.args.get('county_selected')
        # fraction_positive_comply_quarantine = 0.85
        # fraction_contagious_day = float(num_cases_3_weeks)*((1-(fraction_positive_comply_quarantine))+4)/float(total_population)
        # COVID_19_testing_kits_available = float(num_kits_calc)*float(total_population)/1000
        # N95_masks_available = float(num_masks_calc)*float(total_population)/1000
        avg_daily_fatalities = round((float(num_fatalities_7)/float(num_days)),2)
        return render_template("input_fatalities_c3ai_calculate_daily_fatalities.html"
                                ,form=form
                                ,form_date=form_date
                                ,state_selected=state_selected
                                ,county_selected=county_selected
                                ,population_str = total_population
                                ,population = float(total_population.replace(',',''))
                                ,key_contacts_5_17_L1 = float(key_contacts_5_17_L1.replace(',',''))
                                ,key_contacts_18_64_L1=float(key_contacts_18_64_L1.replace(',',''))
                                ,key_contacts_H1=float(key_contacts_H1.replace(',',''))
                                ,key_contacts_H2=float(key_contacts_H2.replace(',',''))
                                ,num_fatalities_daily=num_fatalities_7
                                ,fraction_positive_comply_quarantine = 0.85
                                ,fraction_unknown_cases = 0.8
                                ,fraction_contagious_day=0
                                ,number_contagious_day_5=0
                                ,num_fatalities_7=num_fatalities_7
                                ,fig_fatality_div=fig_fatality_div
                                ,fig_cases_div=fig_cases_div
                                ,avg_daily_fatalities=avg_daily_fatalities
                                ,start_date_fatalities=start_date_fatalities
                                ,end_date_fatalities=end_date_fatalities
                                ,num_days=num_days
                                ,number_sheltered_high_risk=number_sheltered_high_risk
                                ,key_contact_total=key_contact_total
                                ,percent_key_contact_total=percent_key_contact_total
                                , title = 'More Inputs')

    if arg_4=='cases':
        state_selected = request.args.get('state_selected')
        county_selected = request.args.get('county_selected')
        total_population = request.args.get('population')
        key_contacts_5_17_L1 = request.args.get('key_contacts_5_17_L1')
        key_contacts_18_64_L1 = request.args.get('key_contacts_18_64_L1')
        key_contacts_H1 = request.args.get('key_contacts_H1')
        key_contacts_H2 = request.args.get('key_contacts_H2')
        num_fatalities_daily= request.args.get('num_fatalities_daily')
        start_date_fatalities = request.args.get('start_date_fatalities')
        end_date_fatalities = request.args.get('end_date_fatalities')
        avg_daily_fatalities = request.args.get('avg_daily_fatalities')
        num_fatalities_7 = request.args.get('num_fatalities_7')
        num_cases_date = request.args.get('num_cases_date')
        num_days = request.args.get('num_days')
        number_sheltered_high_risk= request.args.get('number_sheltered_high_risk')
        key_contact_total= request.args.get('key_contact_total')
        percent_key_contact_total=request.args.get('percent_key_contact_total')

        date_3_weeks = pd.to_datetime(num_cases_date)
        delta= datetime.timedelta(days=21)
        three_week_date=(date_3_weeks-delta).strftime("%Y-%m-%d")
        # casecounts.columns = ['date','confirmed_cases','confirmed_cases_missing']
        sub_num_cases_data = casecounts[(pd.to_datetime(casecounts.date) >= pd.to_datetime(three_week_date)) & (pd.to_datetime(casecounts.date)<=pd.to_datetime(num_cases_date)) ]
        if not sub_num_cases_data.daily_cases.values.any():
            num_cases_3_weeks = 0
        else:
            num_cases_3_weeks = sub_num_cases_data.daily_cases.sum()
        
        # upper_limit = casecounts[pd.to_datetime(casecounts.dates)==pd.to_datetime(num_cases_date)]
        # lower_limit = casecounts[pd.to_datetime(casecounts.dates)==pd.to_datetime(three_week_date)]
        # num_cases_3_weeks=(upper_limit[colname][0]-lower_limit[colname][0])

        fraction_positive_comply_quarantine = 0.85
        fraction_unknown_cases = 0.8
        fraction_1 = (10/21)*0.2
        fraction_2 = (4.5/21)*4
        fraction_contagious_day = (float(num_cases_3_weeks)*(fraction_1 + fraction_2)/float(total_population))
        Percent_contagious_day = fraction_contagious_day * 100

        ratio_unknown_known_1 = 1
        fraction_2_1 = (4.5/21)*ratio_unknown_known_1
        num_contagious_day_1 = int(float(num_cases_3_weeks)*(fraction_1 + fraction_2_1))
        fr_contagious_day_1 = np.round((float(float(num_cases_3_weeks)*(fraction_1 + fraction_2_1)/float(total_population))*100),4)

        ratio_unknown_known_2 = 2
        fraction_2_2 = (4.5/21)*ratio_unknown_known_2
        num_contagious_day_2 = int(float(num_cases_3_weeks)*(fraction_1 + fraction_2_2))
        fr_contagious_day_2 = np.round((float(float(num_cases_3_weeks)*(fraction_1 + fraction_2_2)/float(total_population))*100),4)

        ratio_unknown_known_3 = 3
        fraction_2_3 = (4.5/21)*ratio_unknown_known_3
        num_contagious_day_3 = int(float(num_cases_3_weeks)*(fraction_1 + fraction_2_3))
        fr_contagious_day_3 = np.round((float(float(num_cases_3_weeks)*(fraction_1 + fraction_2_3)/float(total_population))*100),4)

        ratio_unknown_known_4 = 4
        fraction_2_4 = (4.5/21)*ratio_unknown_known_4
        num_contagious_day_4 = int(float(num_cases_3_weeks)*(fraction_1 + fraction_2_4))
        fr_contagious_day_4 = np.round((float(float(num_cases_3_weeks)*(fraction_1 + fraction_2_4)/float(total_population))*100),4)

        ratio_unknown_known_5 = 5
        fraction_2_5 = (4.5/21)*ratio_unknown_known_5
        num_contagious_day_5 = int(float(num_cases_3_weeks)*(fraction_1 + fraction_2_5))
        fr_contagious_day_5 = np.round((float(float(num_cases_3_weeks)*(fraction_1 + fraction_2_5)/float(total_population))*100),4)


        return render_template("input_fatalities_c3ai_calculate_daily_fatalities_cases.html"
                                ,form=form
                                ,form_date=form_date
                                ,state_selected=state_selected
                                ,county_selected=county_selected
                                ,population_str = total_population
                                ,population = float(total_population.replace(',',''))
                                ,key_contacts_5_17_L1 = float(key_contacts_5_17_L1.replace(',',''))
                                ,key_contacts_18_64_L1=float(key_contacts_18_64_L1.replace(',',''))
                                ,key_contacts_H1=float(key_contacts_H1.replace(',',''))
                                ,key_contacts_H2=float(key_contacts_H2.replace(',',''))
                                ,num_fatalities_daily=num_fatalities_7
                                ,fraction_positive_comply_quarantine = 0.85
                                ,fraction_unknown_cases = 0.8
                                ,fraction_contagious_day=0
                                ,number_contagious_day_5=0
                                ,num_fatalities_7=num_fatalities_7
                                ,fig_fatality_div=fig_fatality_div
                                ,fig_cases_div=fig_cases_div
                                ,avg_daily_fatalities=avg_daily_fatalities
                                ,start_date_fatalities=start_date_fatalities
                                ,end_date_fatalities=end_date_fatalities
                                ,num_cases_3_weeks=num_cases_3_weeks
                                ,num_cases_date=num_cases_date
                                ,num_contagious_day_1=num_contagious_day_1
                                ,fr_contagious_day_1=fr_contagious_day_1
                                ,num_contagious_day_2=num_contagious_day_2
                                ,fr_contagious_day_2=fr_contagious_day_2
                                ,num_contagious_day_3=num_contagious_day_3
                                ,fr_contagious_day_3=fr_contagious_day_3
                                ,num_contagious_day_4=num_contagious_day_4
                                ,fr_contagious_day_4=fr_contagious_day_4
                                ,num_contagious_day_5=num_contagious_day_5
                                ,fr_contagious_day_5=fr_contagious_day_5
                                ,num_days=num_days
                                ,number_sheltered_high_risk=number_sheltered_high_risk
                                ,key_contact_total=key_contact_total
                                ,percent_key_contact_total=percent_key_contact_total
                                , title = 'More Inputs')

    if request.method == 'POST':
        if arg_1=='output':

            # restructure this part :

            # if the route is coming from main then:
                #
                # 0. get all the kits, ppe and vaccine data from forms
                # 1.route=main then calculate
                #     a. number of fatalities - most recent 10 day period
                #     b. num cases - most recent cases
                # 2.route=fatality
                #     a. start and end dates are extracted
                #     b. dailY fatalities are also extracted

            # num_cases_3_weeks = form.num_cases_3_weeks.data
            # num_cases_3_weeks=100
            num_kits_calc= form.num_kits.data
            num_masks_calc= form.num_masks.data
            # num_fatalities_7=form.num_fatalities_7.data
            num_vaccines=form.num_vaccines.data
            fraction_positive_comply_quarantine = 0.85
            
            # num_days=form.num_days.data
            if route1=='main':
                start_date_fatalities = form_date.date_field_cases_start.data
                end_date_fatalities = form_date.date_field_cases_end.data
                num_cases_3_weeks_date = form_date.num_cases_3_weeks_date.data
                number_sheltered_high_risk= request.args.get('number_sheltered_high_risk')
                key_contact_total= request.args.get('key_contact_total')
                percent_key_contact_total=request.args.get('percent_key_contact_total')
                if pd.to_datetime(end_date_fatalities) == pd.to_datetime(start_date_fatalities):
                    num_days = 1
                    sub_fatality_count_data = fatalitycount[(pd.to_datetime(fatalitycount.date) >= pd.to_datetime(start_date_fatalities))]
                    num_fatalities_7 = sub_fatality_count_data.daily_fatalities.sum()
                else:
                    num_days_test = (pd.to_datetime(end_date_fatalities) - pd.to_datetime(start_date_fatalities))
                    num_days = num_days_test.days
                    sub_fatality_count_data = fatalitycount[(pd.to_datetime(fatalitycount.date) >= pd.to_datetime(start_date_fatalities)) & (pd.to_datetime(fatalitycount.date)<=pd.to_datetime(end_date_fatalities)) ]
                    num_fatalities_7 = sub_fatality_count_data.daily_fatalities.sum()

                #extract fatality count between the dates entered
                date_3_weeks = pd.to_datetime(num_cases_3_weeks_date)
                delta= datetime.timedelta(days=21)
                three_week_date=(date_3_weeks-delta).strftime("%Y-%m-%d")
                sub_num_cases_data = casecounts[(pd.to_datetime(casecounts.date) >= pd.to_datetime(three_week_date)) & (pd.to_datetime(casecounts.date)<=pd.to_datetime(num_cases_3_weeks_date)) ]
                if not sub_num_cases_data.daily_cases.values.any():
                    num_cases_3_weeks = 0
                else:
                    num_cases_3_weeks = sub_num_cases_data.daily_cases.sum()
                # upper_limit = casecounts[pd.to_datetime(casecounts.dates)==(pd.to_datetime(three_week_date)+datetime.timedelta(days=1)).strftime(("%Y-%m-%d"))]
                # lower_limit = casecounts[pd.to_datetime(casecounts.dates)==pd.to_datetime(three_week_date)]
                # num_cases_3_weeks=(upper_limit[colname][0]-lower_limit[colname][0])
                fraction_1 = (10/21)*0.2
                fraction_2 = (4.5/21)*4
                fraction_contagious_day = (float(num_cases_3_weeks)*(fraction_1 + fraction_2)/float(total_population))
                Percent_contagious_day = fraction_contagious_day * 100
                # fraction_contagious_day = float(num_cases_3_weeks)*((1-(fraction_positive_comply_quarantine))+4)/float(total_population)
                avg_daily_fatalities = round((float(num_fatalities_7)/float(num_days)),2)

            if route2=='fatality':
                num_cases_3_weeks_date = form_date.num_cases_3_weeks_date.data
                number_sheltered_high_risk= request.args.get('number_sheltered_high_risk')
                key_contact_total= request.args.get('key_contact_total')
                percent_key_contact_total=request.args.get('percent_key_contact_total')
                date_3_weeks = pd.to_datetime(num_cases_3_weeks_date)
                delta= datetime.timedelta(days=21)
                three_week_date=(date_3_weeks-delta).strftime("%Y-%m-%d")
                sub_num_cases_data = casecounts[(pd.to_datetime(casecounts.date) >= pd.to_datetime(three_week_date)) & (pd.to_datetime(casecounts.date)<=pd.to_datetime(num_cases_3_weeks_date)) ]
                if not sub_num_cases_data.daily_cases.values.any():
                    num_cases_3_weeks = 0
                else:
                    num_cases_3_weeks = sub_num_cases_data.daily_cases.sum()
                # upper_limit = casecounts[pd.to_datetime(casecounts.dates)==(pd.to_datetime(three_week_date)+datetime.timedelta(days=1)).strftime(("%Y-%m-%d"))]
                # lower_limit = casecounts[pd.to_datetime(casecounts.dates)==pd.to_datetime(three_week_date)]
                # num_cases_3_weeks=(upper_limit[colname][0]-lower_limit[colname][0])
                fraction_1 = (10/21)*0.2
                fraction_2 = (4.5/21)*4
                fraction_contagious_day = (float(num_cases_3_weeks)*(fraction_1 + fraction_2)/float(total_population))
                Percent_contagious_day = fraction_contagious_day * 100
                # fraction_contagious_day = float(num_cases_3_weeks)*((1-(fraction_positive_comply_quarantine))+4)/float(total_population)
                avg_daily_fatalities = round((float(num_fatalities_7)/float(num_days)),2)

            if route3=='weekly':
                number_sheltered_high_risk= request.args.get('number_sheltered_high_risk')
                key_contact_total= request.args.get('key_contact_total')
                percent_key_contact_total=request.args.get('percent_key_contact_total')
                fraction_1 = (10/21)*0.2
                fraction_2 = (4.5/21)*4
                fraction_contagious_day = (float(num_cases_3_weeks)*(fraction_1 + fraction_2)/float(total_population))
                Percent_contagious_day = fraction_contagious_day * 100
                # fraction_contagious_day = float(num_cases_3_weeks)*((1-(fraction_positive_comply_quarantine))+4)/float(total_population)
                avg_daily_fatalities = round((float(num_fatalities_7)/float(num_days)),2)


            # casecounts_dates_3_weeks = c3aidatalake.evalmetrics(
            #     "outbreaklocation",
            #     {
            #         "spec" : {
            #             "ids" : [id_county_state],
            #             "expressions" : ["JHU_ConfirmedCases"],
            #             "start" : '2020-04-01',
            #             "end" : three_week_date,
            #             "interval" : "DAY",
            #                 }
            #             }
            #         )
            # colname_3_weeks = casecounts_dates_3_weeks.columns[1]
            # num_cases_3_weeks=(casecounts_dates_3_weeks.iloc[-1,:][colname_3_weeks]-casecounts_dates_3_weeks[casecounts_dates_3_weeks.dates==three_week_date][colname_3_weeks][0])
            # # num_cases_3_weeks=cases_from_api

            county_selected = request.args.get('county_selected')

            # fraction_contagious_day = float(num_cases_3_weeks)*((1-(fraction_positive_comply_quarantine))+4)/float(total_population)
            COVID_19_testing_kits_available = float(num_kits_calc)*float(total_population)/1000
            COVID_19_vaccines_available = float(num_vaccines)*float(total_population)/1000
            N95_masks_available = float(num_masks_calc)*float(total_population)/1000
            # avg_daily_fatalities = round((float(num_fatalities_7)/float(num_days)),2)

            # LP Calculations Start here

            list_census_data=[float(total_population),float(key_contacts_5_17_L1),float(key_contacts_18_64_L1),float(key_contacts_H1),float(key_contacts_H2)]
            sheltered_high_risk = float(number_sheltered_high_risk)
            LP_Input = LP_input_function_c3ai(list_census_data,sheltered_high_risk,fraction_contagious_day,COVID_19_vaccines_available,COVID_19_testing_kits_available,N95_masks_available)
            # number_sheltered_high_risk
            #Run for normalcy 0
            normalcy = 0
            #Corresponding Scenario parameter needs to be passed to LP function. Scenario 1 corresponds to Normalcy 0
            #Scenario 10 corresponds to Normalcy 9
            Scenario = "Scenario" + str(normalcy+1)

            TotalPopulation=float(total_population)
            Normalcy_Score,obj_val,obj_coeff,LP_decision = LP_c3ai(LP_Input,Scenario)
            min_activity = LP_Input.query('Parameter1=="min all"')['Scenario1']
            max_activity = LP_Input.query('Parameter1=="max all"')['Scenario1']
            minimum_normalcy = 10*(Normalcy_Score[0]-min_activity[0])/(max_activity[0]-min_activity[0])
            obj_dict = {round(minimum_normalcy,2):obj_val}
            fig_div = dashboard_plots_c3ai(LP_decision)
            figure_dict = {round(minimum_normalcy,2):fig_div}
            scenario_start = math.ceil(minimum_normalcy)
            for i in range(scenario_start,10):
                Scenario_LP = "Scenario" + str(i+1)
                obj_val_i,obj_coeff_i,LP_decision_i = LP_c3ai(LP_Input,Scenario_LP)
                obj_dict[i] = obj_val_i
                # fig_div_i = dashboard_plots(LP_decision_i,obj_val_i,TotalPopulation,county_selected,i)
                # figure_dict[i] = fig_div_i
             #Print the table for normalcy values

            list_normalcy = list(obj_dict.keys())
            list_obj_values = list(obj_dict.values())
            min_obj_key = list_normalcy[0]
            max_obj_key = list_normalcy[-1]
            min_obj_values = round(obj_dict.get(min_obj_key),3)
            max_obj_values = round(obj_dict.get(max_obj_key),3)
            list_first_column = [round(x * (5.15/4.15),3) for x in list_obj_values]
            list_second_column = [round(x ,3) for x in list_obj_values]
            list_third_column = [round(x * (3.15/4.15),3) for x in list_obj_values]
            list_fourth_column = [round(x * (2.15/4.15),3) for x in list_obj_values]
            list_fifth_column = [round(x * (1.15/4.15),3) for x in list_obj_values]

            fig_obj = make_subplots(rows=2, cols=1,vertical_spacing =0.0001,row_heights = [0.07,0.95],
                        specs=[[{"type": "table"}],
                               [{"type": "table"}]])

            fig_obj.add_trace(go.Table(header=dict(values=['<b>Normalcy Scale 0-10</b>','<b>5:1</b>','<b>4:1</b>','<b>3:1</b>','<b>2:1</b>','<b>1:1</b>'],
                                                          line_color='darkslategray',fill_color = 'white',align=['left','center'],font=dict(family='Times New Roman',color='black', size=17),
                                                            height =30),
                                                cells=dict(values=[list_normalcy,list_first_column,list_second_column,list_third_column,
                                                                   list_fourth_column,list_fifth_column],
                                                                   line_color='darkslategray',
                                                           fill_color=['white','white','cyan','white','white','white'],align=['left', 'center'],
                                                           font=dict(family='Times New Roman',color='black', size=17),height =30)),row=2,col=1)


            fig_obj.add_trace(go.Table(header=dict(values=['<b>Ratio of Unknown to Known Cases</b>'],
                                                     line_color='darkslategray',
                            fill_color = ['white'],align=['center'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                                         row=1,col=1)


            fig_obj.update_layout(height=400,margin=dict(l=20,r=20,b=20,t=20))

            fig_obj_div = plotly.offline.plot(fig_obj, include_plotlyjs=False, output_type='div')
            output_choices = list(figure_dict.keys())
            form.normalcy_choices.choices=list_normalcy
            vals = list(figure_dict.values())
            list_LP_decision_values=vals[0]
            return render_template("output_c3ai.html"
                                    ,title='Results'
                                    ,fig_1_div=fig_obj_div
                                    ,form= form
                                    ,min_obj_values=min_obj_values
                                    ,max_obj_values=max_obj_values
                                    ,min_obj_key=min_obj_key
                                    ,num_cases_3_weeks = num_cases_3_weeks
                                    ,COVID_19_testing_kits_available = int(COVID_19_testing_kits_available)
                                    ,N95_masks_available = int(N95_masks_available)
                                    ,num_fatalities_7=num_fatalities_7
                                    ,fraction_positive_comply_quarantine = 0.85
                                    ,fraction_contagious_day = fraction_contagious_day
                                    ,state_selected = state_selected
                                    ,county_selected = county_selected
                                    ,total_population = total_population
                                    ,key_contacts_5_17_L1 = key_contacts_5_17_L1
                                    ,key_contacts_18_64_L1 = key_contacts_18_64_L1
                                    ,key_contacts_H1 = key_contacts_H1
                                    ,key_contacts_H2 = key_contacts_H2
                                    ,avg_daily_fatalities= avg_daily_fatalities
                                    ,num_vaccines=num_vaccines
                                    ,COVID_19_vaccines_available=int(COVID_19_vaccines_available)
                                    ,sheltered_high_risk=sheltered_high_risk
                                    )


        if arg_2=='more':
            norm = form.normalcy_choices.data
            state_selected = request.args.get('state_selected')
            county_selected = request.args.get('county_selected')
            total_population = request.args.get('total_population')
            key_contacts_5_17_L1 = request.args.get('key_contacts_5_17_L1')
            key_contacts_18_64_L1 = request.args.get('key_contacts_18_64_L1')
            key_contacts_H1 = request.args.get('key_contacts_H1')
            key_contacts_H2 = request.args.get('key_contacts_H2')
            fraction_contagious_day=request.args.get('fraction_contagious_day')
            COVID_19_testing_kits_available=request.args.get('COVID_19_testing_kits_available')
            N95_masks_available=request.args.get('N95_masks_available')
            COVID_19_vaccines_available=request.args.get('COVID_19_vaccines_available')
            sheltered_high_risk=request.args.get('sheltered_high_risk')
            avg_daily_fatalities =request.args.get('avg_daily_fatalities')
            # COVID_19_testing_kits_available=(float(num_kits_calc)*float(total_population))/1000
            # N95_masks_available=float(num_masks_calc)*float(total_population)/1000

            sum_key_contact = float(key_contacts_5_17_L1)+float(key_contacts_18_64_L1)+float(key_contacts_H1)+float(key_contacts_H2)
            percent_key_pop = np.round((sum_key_contact/float(total_population))*100,2)
            list_census_data=[float(total_population),float(key_contacts_5_17_L1),float(key_contacts_18_64_L1),float(key_contacts_H1),float(key_contacts_H2)]
            LP_Input = LP_input_function_c3ai(list_census_data,float(sheltered_high_risk),float(fraction_contagious_day),float(COVID_19_vaccines_available),float(COVID_19_testing_kits_available),float(N95_masks_available))
            # return str(COVID_19_testing_kits_available)
            #User enters normalcu
            normalcy = math.ceil(float(norm))
            #Corresponding Scenario parameter needs to be passed to LP function. Scenario 1 corresponds to Normalcy 0
            #Scenario 10 corresponds to Normalcy 9
            Scenario = "Scenario" + str(normalcy+1)
            # test_var=(LP_Input.query('Parameter1=="p" and Parameter2=="+"')[Scenario])
            #LP_c3ai(LP_Input,Scenario_LP)
            obj_val,obj_coeff,LP_decision = LP_c3ai(LP_Input,Scenario)
            # return str(obj_val)
            figures_div = dashboard_plots_c3ai(LP_decision)
            #{"fig3":fig_3_div,"fig4":fig_4_div,"fig5":fig_5_div,"fig6":fig_6_div,"fig7":fig_7_div,"fig8":fig_8_div}

            # fig_test=request.args.get('list_LP_decision_values')
            # list_normalcy= request.args.get('list_normalcy')
            # # return list_normalcy
            # list_obj_values= request.args.get('list_obj_values')
            # list_LP_decision_values= request.args.get('list_LP_decision_values')
            # output_choices= request.args.get('output_choices')
            # normalcy_level = form_new.normalcy_choices.data
            # TotalPopulation=total_population
            # i=list_normalcy.index('9')
            # return normalcy_level
            # LP_decision_i = list_LP_decision_values[i]
            # obj_val_i = list_obj_values[i]
            # # obj_val_i = list_obj_values.index(normalcy_level)
            # figures_div = dashboard_plots(LP_decision_i,obj_val_i,TotalPopulation,county_selected,i)
            return render_template("extra_outputs_c3ai.html"
                                    ,title='More Results'
                                    ,normalcy=normalcy
                                    ,state_selected=state_selected
                                    ,county_selected=county_selected
                                    # ,population_str = "{:,}".format(total_population)
                                    ,population=total_population
                                    ,key_contacts_5_17_L1 = "{:,}".format(int(float(key_contacts_5_17_L1)))
                                    ,key_contacts_18_64_L1="{:,}".format(int(float(key_contacts_18_64_L1)))
                                    ,key_contacts_H1="{:,}".format(int(float(key_contacts_H1)))
                                    ,key_contacts_H2="{:,}".format(int(float(key_contacts_H2)))
                                    ,sum_key_contact="{:,}".format(int(float(sum_key_contact)))
                                    ,percent_key_pop=percent_key_pop
                                    ,COVID_19_testing_kits_available=int(COVID_19_testing_kits_available)
                                    ,N95_masks_available=int(N95_masks_available)
                                    ,COVID_19_vaccines_available=int(COVID_19_vaccines_available)
                                    # ,fig_2_div=figures_div[0]
                                    ,fig_3_div=figures_div.get('fig3')
                                    ,fig_4_div=figures_div.get('fig4')
                                    ,fig_5_div=figures_div.get('fig5')
                                    ,fig_6_div=figures_div.get('fig6')
                                    ,fig_7_div=figures_div.get('fig7')
                                    ,fig_8_div=figures_div.get('fig8')
                                    ,avg_daily_fatalities=avg_daily_fatalities
                                    ,obj_val=np.round(obj_val,2)
                                    )


    else:
        return render_template("input_fatalities_c3ai.html"
                                ,form=form
                                ,form_date=form_date
                                ,state_selected=state_selected
                                ,county_selected=county_selected
                                ,population_str = total_population
                                ,population = float(total_population.replace(',',''))
                                ,key_contacts_5_17_L1 = float(key_contacts_5_17_L1.replace(',',''))
                                ,key_contacts_18_64_L1=float(key_contacts_18_64_L1.replace(',',''))
                                ,key_contacts_H1=float(key_contacts_H1.replace(',',''))
                                ,key_contacts_H2=float(key_contacts_H2.replace(',',''))
                                ,num_fatalities_daily=0
                                ,fraction_positive_comply_quarantine = 0.85
                                ,fraction_unknown_cases = 0.8
                                ,fraction_contagious_day=0
                                ,number_contagious_day_5=0
                                ,cases_from_api=0
                                ,fig_fatality_div=fig_fatality_div
                                ,fig_cases_div=fig_cases_div
                                ,today=today
                                ,number_sheltered_high_risk=number_sheltered_high_risk
                                ,key_contact_total=key_contact_total
                                ,percent_key_contact_total=percent_key_contact_total
                                ,avg_daily_fatalities=0
                                , title = 'More Inputs')

                                
@app.route('/county/<state>')
def county(state):
    state = state.replace("%20"," ")
    counties = counties_dict.get(state)
    counties.sort()
    return jsonify({'counties':counties})


if __name__ == '__main__':
    app.run(debug=True)
