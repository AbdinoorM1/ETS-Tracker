"""
Project: ETS Tracker.py
Author: Abdinoor Moallin
Date: September 2025 - November 2025

Description:
    Interactive Python GUI for exploring Edmonton Transit Service (ETS) routes.
    Users can search for bus routes by selecting origin and destination stops.
    Routes are plotted on a map using graphics.py, with service disruptions displayed as red markers.
    Supports functionality to load, save, and visualize route, shape, and disruption data.

Libraries:
    pickle, graphics.py, datetime
"""
import pickle 
from graphics import *
from datetime import date 
    
def route_data():
    '''
    purpose: loads route data  
    parameters: 
    return:route_d
    '''        
    route_d = {}
    file_name = input("Enter a filename: ").strip() 
    if file_name == "": #scenario 3
        file_name = "data/trips.txt" #adding to empty string
        file_check = open("data/trips.txt","r")
        print(f"Data from {file_name} loaded")

    else: #if its not a space 
        
        try: #scenario 2
            file_check = open(file_name,"r")
            print(f"Data from {file_name} loaded")
        
        except FileNotFoundError: #scenario 1
            print(f"IO Error: Couldn't open {file_name}") 
            return None 

    lines = file_check.readlines()
    file_check.close()
    #clean_location
        
    for line in range(1, len(lines)):#Skip header
        clean_lines = lines[line].split(",")
        route_id = clean_lines[0]
        shape_id = clean_lines[6].strip()
        location = clean_lines[3].strip().replace('"', "").lower()

        if route_id not in route_d:
            route_d[route_id] = [[shape_id], [location]]
        else:
            if shape_id not in route_d[route_id][0]:
                route_d[route_id][0].append(shape_id)
            if location not in route_d[route_id][1]:
                route_d[route_id][1].append(location)

    return route_d
    
    
def load_shape() -> dict:
    '''
    purpose: load data shapes 
    parameters: none 
    return: shape_d
    '''
    file = input('Enter filename: ').strip() 
    if file == '':
        file = 'data/shapes.txt'
    
    try: 
        f = open(file, 'r') 
    except IOError: 
        print(f'problem loading {file}, try again') 
        return
    
    lines = f.readlines() 
    f.close() 
    
    shape_d = {} 
    for i in range(1, len(lines)): 
        clean = lines[i].strip('\n')  
        lst = clean.split(',')
        shape_id = lst[0]
        coords = (float(lst[2]),float(lst[1])) 
        
        if shape_id not in shape_d: 
            shape_d[shape_id] = [coords]
        else: 
            shape_d[shape_id].append(coords) 
    
    print(f'Data from {file} successfully loaded')
    return shape_d


def load_disruptions(month_dict):
    '''
    purpose: loads disruption data, stores dates and coords in dictionary 
    parameters: month_dict
    return:disruption_d
    '''    
    disruption_d = {}#keys will be coordinates, values are the dates
    #since the coordinates are unique and the dates aren't, coords are the keys!
    file_choice = input("Enter a filename to load: ")
    
    if file_choice == "":
        file_choice = "data/traffic_disruptions.txt"
        try:
            open_file = open(file_choice,"r")
            print(f"Data from {file_choice} loaded")
        except FileNotFoundError:
            print("We got a problem ")
            
    else:
        try:
            open_file = open(file_choice,"r")
            print(f"Data from {file_choice} loaded")
        
        except IOError:
            return f"IO Error: {file_choice} not loaded"
        
    file_lines = open_file.readlines()  
    open_file.close()
    lst = []

    for line in file_lines[1:]: #skip headers [1:]
        lst.append(line.strip().split(","))
    
    for item in lst:
        month_day = item[5].strip(",").split()

        year = int(str(item[6]).strip('"'))
        point = str((item[-1].strip("POINT")).strip('"')).strip()
        month_name = str(month_day[0]).strip('"')
        
        points = point.split()
        p1 = float(points[0].strip("("))
        p2 = float(points[1].strip(")"))
        complete_points = p1,p2
        complete_coords= tuple(complete_points) #tuple of points 1 & 2
        
        if month_name in month_dict:
            month_num = month_dict[month_name]
            
        day = int(str(month_day[1]).strip())
        dates = str(date(year,month_num,day)) #making the dates
        
        if point not in disruption_d: #add data into dictionary
            disruption_d[complete_coords] = ""
            disruption_d[complete_coords] += dates
    return disruption_d


def print_shape_ids(route_d:dict):
    '''
    purpose: prints shape id's for a route  
    parameters:route_d
    return:None
    '''
    route_choice = input("Enter Route: ").strip()

    if route_choice not in route_d:
        print("\t** NOT FOUND **")
    else:
        shape_ids = route_d[route_choice][0] 
        locations = route_d[route_choice][1] 
        location_str = ""
        for places in locations:
            if location_str:
                location_str += " - "
            location_str += places
       
        # Display the result
        print(f"Shape ids for route {route_choice} at location {location_str}:")
        for shape_id in shape_ids:
            print(f"\t{shape_id}")


def print_coords(shape_d:dict): 
    '''
    purpose: print coords to shape 
    parameters: shape_d 
    return: None
    '''   
    shape = input('Enter shape_id: ').strip()
    if shape not in shape_d.keys(): 
        print('\t**NOT FOUND**') 
    else: 
        print(f'Shape ID coordinates {shape} are: ')
        for coords in shape_d.get(shape): 
            print('\t', coords)


def print_longest(route_d:dict, shape_d:dict):
    '''
    purpose: print longest coords
    parameters: route_d, shape_d
    return: longest
    '''  
    longest = ''
    coord_count = 0
    route = input('Enter route ID: ').strip()
    if route not in route_d.keys():
        print('\t** NOT FOUND **')
    else:
        shape_ids = route_d[route][0]
        for shape in shape_ids:
            if shape in shape_d:
                count = len(shape_d[shape])
                if count > coord_count:
                    coord_count = count
                    longest = shape
       
        print(f'the longest shape for {route} is {longest} with {coord_count} coordinates')
    return longest

        
def save_pickle(route_d:dict, shape_d:dict, ld_disruption:dict):
    '''
    purpose: data structures containing route&shapes data saved to binary file 
    parameters: route_d, shape_d, disruption_d
    return:None
    ''' 
    file_prompt = input("Enter a filename: ").strip()
    
    if file_prompt == "":
        file_prompt = "data/etsdata.p."
    
    try:
        stored = open(file_prompt,"wb")
        print(f"Data structures successfully written to {file_prompt}")
        
    except IOError:
        print("unable to display file")

    pickle.dump(route_d,stored)
    pickle.dump(shape_d,stored)
    pickle.dump(ld_disruption,stored)
    stored.close()


def load_pickle(s:bool, c:bool, d:bool): 
    '''
    purpose: read data structures from the pickled file 
    parameters: s, c, d
    return: None
    '''     
    file = input('Enter a filename: ').strip()
    if file == '':
        file = 'data/etsdata.p.'
    
    try: 
        f = open(file, 'rb')
        ld_route = pickle.load(f) 
        ld_shape = pickle.load(f)
        ld_disruption = pickle.load(f) 
    except FileNotFoundError: #by using this except, there is no need for p_count and the if statement in main 
        print('Data not pickled yet')
        return
    except IOError as ie:
        print(ie)
        return
    except Exception as e:
        print(e)
        return
    finally: 
        f.close() 
        s = True
        c = True
        d = True
          
    print(f'Routes and shapes data structures successfully loaded from {file}')
    return ld_route, ld_shape, ld_disruption, s, c, d
    
    
#----------------------------------------------
#all GUI elements start here  


def edmonton_map(): 
    '''
    purpose: display edmonton map 
    parameters: none 
    return: win
    '''  
    win = GraphWin('ETS Tracker', 800, 920) 

    # Set world coordinate system FIRST
    win.setCoords(-113.720049, 53.393703, -113.320418, 53.657116)

    # Compute midpoint in *map coordinates*
    imgw = (-113.720049 + -113.320418) / 2
    imgh = (53.393703  +  53.657116) / 2

    # Draw the map
    edmonton = Image(Point(imgw, imgh), 'edmonton.png')
    edmonton.draw(win)
    return win
    
    
def from_box(win):
    '''
    purpose: display from box and get location
    parameters: win
    return:  user_from
    '''
    fro_text = Text(Point(-113.709, 53.639), 'From:') 
    fro_text.setStyle('bold')
    fro_text.setSize(16)
    fro_text.draw(win)
    
    user_from = Entry(Point(-113.660, 53.639), 18) 
    user_from.setFill('white')    
    user_from.draw(win)    
    
    return user_from    


def to_box(win): 
    '''
    purpose: display to box and get location 
    parameters: win 
    return: user_to
    '''         
    
    to_text = Text(Point(-113.709, 53.630), 'To:') 
    to_text.setStyle('bold')
    to_text.setSize(16)
    to_text.draw(win)
    user_to = Entry(Point(-113.660, 53.629),18)
    user_to.setFill('white')
    user_to.draw(win)
    
    return user_to


def search(win):
    '''
    purpose: search button
    parameters: win 
    return: None
    '''  
    srch = Rectangle(Point(-113.694,53.623), Point(-113.626,53.617))
    
    srch.setFill('yellow')
    srch.draw(win)
    
    srch_text = Text(Point(-113.66,53.6195), 'Search') 
    srch_text.setStyle('bold')    
    srch_text.draw(win) 
    
    
def get_longest_shape_for_route(route_id, route_d, shape_d):
    """
    Return the shape_id (str) with the most coordinates for route_id.
    Returns longest/None
    """
    longest = ''
    max_len = 0
    if route_id not in route_d:
        return longest

    shape_ids = route_d[route_id][0]
    for s in shape_ids:
        if s in shape_d:
            length = len(shape_d[s]) # shape_d[s] == list of coords
            if length > max_len:
                max_len = length
                longest = s
    return longest


def search_func(win, fro, to, route_d, shape_d): 
    '''
    purpose: functionality of search function (finds shortest route, plots routes)
    parameters: win, fro, to, route_d, shape_d
    return: None
    '''     
    msg_point = Point(-113.66, 53.595)

    for item in win.items[:]:
        if isinstance(item, Text):
            y = item.getAnchor().getY()
            if 53.594 <= y <= 53.596:  # message display line
                try:
                    item.undraw()
                    win.items.remove(item)
                except ValueError:
                    pass

    from_text = fro.getText().strip().lower()
    to_text = to.getText().strip().lower()

    if from_text == "" and to_text == "":
        not_found = Text(msg_point, 'NOT FOUND')
        not_found.setSize(14)
        not_found.setStyle('bold')
        not_found.setTextColor('black')
        not_found.draw(win)
        return

    matching_routes = []
    for route_id, val in route_d.items():
        locations = [stop.lower() for stop in val[1]]
        if any(from_text in stop for stop in locations) and any(to_text in stop for stop in locations):
            matching_routes.append(route_id)

    if not matching_routes:
        not_found = Text(msg_point, 'NOT FOUND')
        not_found.setSize(14)
        not_found.setStyle('bold')
        not_found.setTextColor('black')
        not_found.draw(win)
        return

    shortest_route = None
    min_len = None
    for route_id in matching_routes:
        longest_shape_id = get_longest_shape_for_route(route_id, route_d, shape_d)
        if longest_shape_id and longest_shape_id in shape_d:
            length = len(shape_d[longest_shape_id])
            if (min_len is None) or (length < min_len):
                min_len = length
                shortest_route = route_id

    if shortest_route is None:
        not_found = Text(msg_point, 'NOT FOUND')
        not_found.setSize(14)
        not_found.setStyle('bold')
        not_found.setTextColor('black')
        not_found.draw(win)
        return

    found_route = shortest_route

    msg = Text(msg_point, f'Drawing route {found_route}')
    msg.setSize(16)
    msg.setStyle('bold')
    msg.setTextColor('black')
    msg.draw(win)

    
    longest_shape_id = get_longest_shape_for_route(found_route, route_d, shape_d)
    #^route drawing:
    coordinates = shape_d[longest_shape_id]
    if len(coordinates) > 1:
        n = 10
        for i in range(0, len(coordinates) - n, n):
            lon1, lat1 = coordinates[i]
            lon2, lat2 = coordinates[i + n]
            line = Line(Point(lon1, lat1), Point(lon2, lat2))
            line.setWidth(2)
            line.setFill("blue")
            line.draw(win)
    
               
def clear(win):
    '''
    purpose: clear button
    parameters: win
    return: None
    '''      
    clr = Rectangle(Point(-113.694,53.614), Point(-113.626,53.608))
    
    clr.setFill('yellow') 
    clr.draw(win)
    
    clr_text = Text(Point(-113.66,53.611), 'Clear Text') 
    clr_text.setStyle('bold')
    clr_text.draw(win)


def clear_func(win, user_from, user_to): 
    '''
    purpose: functionality of clear button
    parameters: win, user_from, user_to
    return: None
    '''        
    # setText returns None, don't reassign to user_from/user_to
    user_from.setText('')
    user_to.setText('')
    
    
def clear_routes(win):
    clear_routes_box = Rectangle(Point(-113.694,53.605),Point(-113.626,53.599))
    clear_routes_box.setFill('yellow') 
    clear_routes_box.draw(win)
    clear_text = Text(Point(-113.66,53.6015),'Clear Routes') 
    clear_text.setStyle('bold')
    clear_text.draw(win)    
               
               
def dis_plot(win,disruption_d):
    """
    Purpose: Plots disruption points (can give another year's data if needed)
    Parameters: win,disruption_d
    Return: None
    """    
    #dis_d = disruption(month_dict)
    #print(dis_d)
    todays_date = str(date.today())
    #print(f"todays date: {todays_date}, type{type(todays_date)}")
    
    for coords in disruption_d.keys():
        disruption_date = disruption_d[coords]   
        #print(disruption_date)
        if disruption_date >= todays_date: 
            #want to check for disruptions that are ending either today or in the future
            #the disruption data is for 2024/2025, if demoing this at a later date, will need to update the disruptions by getting the dataset from Edmonton data (ETS disruptions)
            lon,lat = coords
            point = Point(lon,lat) 
            circle = Circle(point,0.0010)
            circle.setFill("red")
            circle.setOutline("red")
            circle.draw(win)
        
    
def graph_main(route_d,shape_d,disruption_d):
    '''
    purpose: all graph elements 
    parameters: route_d, shape_d,disruption_d
    return: None
    '''  
    win = edmonton_map()
    fro = from_box(win)    
    to = to_box(win)
    search(win)
    clear(win) 
    clear_routes(win)
    dis_plot(win,disruption_d)
        
    running = True
    while running:
        try:
            pt = win.checkMouse()  # non-blocking mouse click
            key = win.checkKey()
            
        except GraphicsError:
            
            break

        if key == "Return":   # Enter pressed
            search_func(win, fro, to, route_d, shape_d)

        if pt:
            x, y = pt.getX(), pt.getY()
            
            # search check:
            if (-113.694 <= x <= -113.626) and (53.617 <= y <= 53.623):
                search_func(win, fro, to, route_d, shape_d)
                
            # clear text check:
            elif (-113.694 <= x <= -113.626) and (53.608 <= y <= 53.614):
                clear_func(win, fro, to)
                
            # clear all check (lines + message + reset text):
            elif (-113.694 <= x <= -113.626) and (53.599 <= y <= 53.605):
                for item in win.items[:]:
                    if isinstance(item, Line):
                        try:
                            item.undraw()
                        except:
                            pass
                
                   
#----------------------------------------------

def print_menu(): 
    '''
    purpose: print menu to clear up the main function 
    parameters: none 
    return: None
    '''    
    print('\nEdmonton Transit System') 
    print('-' * 20) 
    print('(1) Load route data')
    print('(2) Load shapes data') 
    print('(3) Load disruptions data\n')
    print('(4) Print shape IDs for a route')
    print('(5) Print coordinates for a shape ID')
    print('(6) Find Longest shape for route\n')
    print('(7) Save routes and shapes in a pickle')
    print('(8) Load routes and shapes from a pickle')
    print('(9) Interactive map')
    print('(0) Quit')    
           
                
def main(): 
    '''
    purpose: main function 
    parameters: none 
    return: None
    '''  
    print_menu()
    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12} #used for load disruption data
    choice = '' 
    s = False #both used to track if user has entered data 
    c = False #changed from a int counter to bool
    d = False
    win_open = False #used to detect if window is open
    while choice != '0':
        #print_menu()
        choice = input('\nEnter command: ').strip()
        if choice not in ['0','1','2','3','4','5','6','7','8','9']: 
            print('Invalid Option') 
        elif choice == '0':
            return #exit the choice prompts
        elif choice == '1': 
            ld_route = route_data()            
            s = True
        elif choice == '2':
            ld_shape = load_shape()
            c = True
        elif choice == '3':
            ld_disruption = load_disruptions(month_dict) #returned dict 
            d = True
        elif choice == '4':
            if s: 
                print_shape_ids(ld_route)
            
            else: 
                print("Route data hasn't been loaded yet")    
        elif choice == '5': 
            if c: 
                print_coords(ld_shape)
            else:
                print("Shape ID data hasn't been loaded yet") 
        elif choice =='6': 
            if s and c: 
                print_longest(ld_route, ld_shape)
            else: 
                print('data not loaded yet, please try again')
        elif choice == "7":
            if s and c and d:   
                p_dump = save_pickle(ld_route, ld_shape, ld_disruption)  
            else:
                print("All data has not been loaded yet, please try again")
        elif choice == '8': 
            result = load_pickle(s,c,d)
            if result:
                ld_route, ld_shape, ld_disruption, s, c, d = result
        elif choice == '9': 
            if s and c and d:
                win_open = True
                graph_main(ld_route,ld_shape,ld_disruption)
                print_menu()
            else:
                print("You must load all data first!")
            
if __name__ == "__main__":
    main()