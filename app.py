from flask import Flask, render_template, request, session, redirect, url_for
import os
import random

app = Flask(__name__)
# Use a secure secret key from environment variables, fallback to a default for local testing
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

class Node:
    node_counter = 0  # To assign unique IDs to nodes

    def __init__(self, text):
        self.text = text.strip()
        self.yes = None
        self.no = None
        self.id = Node.node_counter  # Assign a unique ID
        Node.node_counter += 1

def parse_tree(tree_text):
    lines = tree_text.split('\n')
    lines = [line.replace('\t', '    ') for line in lines]
    node_stack = {}
    last_action = {}
    root = None
    for line in lines:
        if not line.strip():
            continue
        stripped_line = line.lstrip(' ')
        indent = len(line) - len(stripped_line)
        depth = indent // 4
        line_text = stripped_line.strip()
        if 'YES:' in line_text or 'NO:' in line_text:
            if 'YES:' in line_text:
                action, rest = line_text.split('YES:', 1)
                action = 'YES'
            else:
                action, rest = line_text.split('NO:', 1)
                action = 'NO'
            rest = rest.strip()
            if rest:
                node = Node(rest)
                parent = None
                for i in range(depth - 1, -1, -1):
                    if i in node_stack and node_stack[i]:
                        parent = node_stack[i]
                        break
                if parent:
                    if action == 'YES':
                        parent.yes = node
                    else:
                        parent.no = node
                else:
                    root = node
                node_stack[depth] = node
                last_action[depth] = None
            else:
                last_action[depth] = action
                node_stack[depth] = None
        else:
            node = Node(line_text)
            parent = None
            for i in range(depth - 1, -1, -1):
                if i in node_stack and node_stack[i]:
                    parent = node_stack[i]
                    break
            action = None
            for i in range(depth, -1, -1):
                if i in last_action and last_action[i]:
                    action = last_action[i]
                    last_action[i] = None
                    break
            if parent and action:
                if action == 'YES':
                    parent.yes = node
                else:
                    parent.no = node
            else:
                root = node
            node_stack[depth] = node
    return root

def store_nodes(node, nodes_dict):
    nodes_dict[str(node.id)] = {
        'text': node.text,
        'yes': node.yes.id if node.yes else None,
        'no': node.no.id if node.no else None
    }
    if node.yes:
        store_nodes(node.yes, nodes_dict)
    if node.no:
        store_nodes(node.no, nodes_dict)

# Initialize nodes_dict as a global variable
nodes_dict = {}

# Parsing Trees
tree_text1 = """
Is your country in Asia?
    YES:
        Is your country a muslim majority country?
            YES:
                Is your country population greater than 25 million?
                    YES:
                        In general,is your country considered middle east?
                            YES:
                                Is your country located in arabian peninsula?
                                    YES:
                                        Is your country a monarchy?
                                            YES:Saudi Arabia
                                            NO:Yemen
                                    NO:
                                        Is your country a theocracy?
                                            YES:Iran
                                            NO:
                                                Does your country have mediterranean sea coast?
                                                    YES:Turkey
                                                    NO:Iraq
                            NO:
                                In broader sense is your country considered a south asian country?
                                    YES:
                                        Does your country possess nuclear weapons?
                                            YES:Pakistan
                                            NO:
                                                Is your country landlocked?
                                                    YES:Afghanistan
                                                    NO:Bangladesh
                                    NO:
                                        Is your country landlocked?
                                            YES:Uzbekistan
                                            NO:
                                                Is your country a monarchy?
                                                    YES:Malaysia
                                                    NO:Indonesia
                    NO:
                        Is your country in middle east?
                            YES:
                                Is your country a GCC member?
                                    YES:
                                        Does your country border at least 2 or more countries?
                                            YES:
                                                Is your nation a federation as opposed to a unitary state?
                                                    YES:UAE
                                                    NO:
                                                        Is your nation an absolute monarchy?
                                                            YES:Oman
                                                            NO:Kuwait
                                            NO:
                                                Is your country an island?
                                                    YES:Bahrain
                                                    NO:Qatar
                                    NO:
                                        Does your country border dead sea?
                                            YES:
                                                Does your country border Mediterranean sea?
                                                    YES:Palestine
                                                    NO:Jordan
                                            NO:
                                                Does your country border 3 or more countries?
                                                    YES:Syria
                                                    NO:Lebanon
                            NO:
                                Is your country generally considered as a central Asian republic?
                                    YES:
                                        Does your country have a Caspian Sea coast?
                                            YES:
                                                Is your country one of the top 10 largest countries in the world?
                                                    YES:Kazakhstan
                                                    NO:Turkmenistan
                                            NO:
                                                Is your country a member of the Organization of Turkic States?
                                                    YES:Kyrgyzstan
                                                    NO:Tajikistan
                                    NO:
                                        Is your country a former Soviet republic?
                                            YES:Azerbaijan
                                            NO:
                                                Is your country a monarchy?
                                                    YES:Brunei
                                                    NO:Maldives
            NO:
                Is the population of your country greater than 25 million?
                    YES:
                        Does your country have any currently operational nuclear power plant?
                            YES:
                                Does your country have nuclear weapons?
                                    YES:
                                        Is your country Hindu majority by population?
                                            YES:India
                                            NO:China
                                    NO:
                                        Is your country considered an island nation?
                                            YES:Japan
                                            NO:South Korea
                            NO:
                                Does your nation's language script have significant Indian influence?
                                    YES:
                                        Is your country landlocked?
                                            YES:Nepal
                                            NO:
                                                Does your nation share a border with India?
                                                    YES:Myanmar
                                                    NO:Thailand
                                    NO:
                                        Is your country an island nation?
                                            YES:Philippines
                                            NO:
                                                Does your country have nuclear weapons?
                                                    YES:North Korea
                                                    NO:Vietnam
                    NO:
                        Is Buddhism the largest religion in your country?
                            YES:
                                Is your country landlocked?
                                    YES:
                                        Does your country border India?
                                            YES:Bhutan
                                            NO:
                                                Does your country border at least 3 countries?
                                                    YES:Laos
                                                    NO:Mongolia
                                    NO:
                                        Is your nation an island nation?
                                            YES:
                                                Is your nation a city-state?
                                                    YES:Singapore
                                                    NO:Sri Lanka
                                            NO:Cambodia
                            NO:
                                Is your country an island nation?
                                    YES:
                                        Is your country a member of the EU?
                                            YES:Cyprus
                                            NO:East Timor
                                    NO:
                                        Is your country a former Soviet republic?
                                            YES:
                                                Does your country have a Black Sea coast?
                                                    YES:Georgia
                                                    NO:Armenia
                                            NO:Israel
"""

tree_text2 = """
In geographical sense, is your country in the Americas or Europe?
    YES:
        Is Spanish the majority language in your country?
            YES:
                Is your country in South American continental Landmass?
                    YES:
                        Is your country's population greater than 25 million?
                            YES:
                                Does your country have a Pacific Ocean coast?
                                    YES:
                                        Does your country's flag have vertical stripes?
                                            YES:Peru
                                            NO:Colombia
                                    NO:
                                        Did your country ever win the FIFA World cup?
                                            YES:Argentina
                                            NO:Venezuela
                            NO:
                                Is your country Landlocked?
                                    YES:
                                        Does your country share border with atleast 4 countries:
                                            YES:Bolivia
                                            NO:Paraguay
                                    NO:
                                        Does your country have a Pacific Coast?
                                            YES:
                                                Does your country has a territorial claim on Antarctica?
                                                    YES:Chile
                                                    NO:Ecuador
                                            NO:Uruguay
                    NO:
                        Is your country's population greater than 15 million?
                            YES:
                                Is your country in Europe?
                                    YES:Spain
                                    NO:
                                        Is Peso your country's currency?
                                            YES:Mexico
                                            NO:Guatemala
                            NO:
                                Does your country have both Pacific and Atlantic coasts?
                                    YES:
                                        Does your country have a standing army?
                                            YES:
                                                Does your country border atleast 3 countries?
                                                    YES:Honduras
                                                    NO:Nicaragua
                                            NO:
                                                Does your country have any canal that connects Pacific and Atlantic ocean?
                                                    YES:Panama
                                                    NO:Costa Rica
                                    NO:
                                        Is your country an island country:
                                            YES:
                                                Is your country a one-party state?
                                                    YES:Cuba
                                                    NO:Dominican Republic
                                            NO:El Salvador
            NO:
                Is your country in Europe:
                    YES:
                        Was your country(full territory) considered a communist nation in 20th century?
                            YES:
                                Is your country in European Union?
                                    YES:
                                        Is Euro the official currency of your nation?
                                            YES:
                                                Is your country a Baltic State?
                                                    YES:
                                                        Is Roman Catholic the prominant branch of christianity in your nation?
                                                            YES:Lithuania
                                                            NO:
                                                                Does your country's language belong in Indo-European language family:
                                                                    YES:Latvia
                                                                    NO:Estonia
                                                    NO:
                                                        Is your country a former yugoslav republic?
                                                            YES:
                                                                Does your country have more than a thousand islands?
                                                                    YES:Croatia
                                                                    NO:Slovenia
                                                            NO:Slovakia
                                            NO:
                                                Does your nation have a black sea coast?
                                                    YES:
                                                        Is your country's language a slavic language?
                                                            YES:Bulgaria
                                                            NO:Romania
                                                    NO:
                                                        Is your country landlocked?
                                                            YES:
                                                                Is your country's language a slavic language?
                                                                    YES:Czech Republic
                                                                    NO:Hungary
                                                            NO:Poland

                                    NO:
                                        Is your country a former Yugoslav Republic?
                                            YES:
                                                Is your nation in NATO?
                                                    YES:
                                                        Is your nation landlocked?
                                                            YES:North Macedonia
                                                            NO:Montenegro
                                                    NO:
                                                        Is your nation landlocked?
                                                            YES:Serbia
                                                            NO:Bosnia and Herzegovina
                                            NO:
                                                Is your nation landlocked(No coastline)?
                                                    YES:
                                                        Is your country a presidential republic?
                                                            YES:Belarus
                                                            NO:Moldova
                                                    NO:
                                                        Does your country have Black Sea coast?
                                                            YES:Ukraine
                                                            NO:Albania
                            NO:
                                Is your country in European Union(EU)?
                                    YES:
                                        Is your country a monarchy?
                                            YES:
                                                Is your country a scandinavian country?
                                                    YES:
                                                        Does your country share border with just one country?
                                                            YES:Denmark
                                                            NO:Sweden
                                                    NO:
                                                        Is your country a landlocked country?
                                                            YES:Luxembourg
                                                            NO:
                                                                 Does your country border France?
                                                                    YES:Belgium
                                                                    NO:Netherlands
                                            NO:
                                                Does your country directly controled any oversee colonies?
                                                    YES:
                                                        Does your country have a Mediterraean coast?
                                                            YES:
                                                                Is your country nuclear armed?
                                                                    YES:France
                                                                    NO:Italy
                                                            NO:
                                                                Does your country share border with just one country?
                                                                    YES:Portugal
                                                                    NO:Germany
                                                    NO:
                                                        Is your country a member of NATO?
                                                            YES:
                                                                Does your country have mediterraean coast?
                                                                    YES:Greece
                                                                    NO:Finland
                                                            NO:
                                                                Is english the official language of your country?
                                                                    YES:
                                                                        Does your country share border with any other country?
                                                                            YES:Ireland
                                                                            NO:Malta
                                                                    NO:
                                                                        Is your country landlocked?
                                                                            YES:Austria
                                                                            NO:Cyprus
                                    NO:
                                        Is your country landlocked?
                                            YES:
                                                Is your country entirely enclaved by a single other country?
                                                    YES:
                                                        Is your country the seat of Pope?
                                                            YES:Vatican City
                                                            NO:San Marino
                                                    NO:
                                                        Is your nation considered a micro-nation?
                                                            YES:
                                                                Is german the predominant language in your nation?
                                                                    YES:Liechtenstein
                                                                    NO:Andorra
                                                            NO:Switzerland
                                            NO:
                                                Is your nation an island nation:
                                                    YES:
                                                        Is your nation Nuclear armed?
                                                            YES:United Kingdom
                                                            NO:Iceland
                                                    NO:
                                                        Is your nation considered a micro-nation?
                                                            YES:Monaco
                                                            NO:Norway
                    NO:
                        Is your country a Caribbean Island nation?
                            YES:
                                Is your country a constitutional monarchy?
                                    YES:
                                        Does your country gain independence after 1975?
                                            YES:
                                                # It seems incomplete in original code. You may need to complete it.
                                    NO:
                                        Is your country population greater than one million?
                                            YES:
                                                Is your country located on the island of hispaniola?
                                                    YES:Haiti
                                                    NO:Trinidad and Tobago
                                            NO:
                                                Did your nation became republic from constitutional monarchy in 21st century?
                                                    YES:Barbados
                                                    NO:Dominica
                            NO:
                                Is your country in NATO?
                                    YES:
                                        Is your country nuclear armed?
                                            YES:United States
                                            NO:Canada
                                    NO:
                                        Is english the official language in your country?
                                            YES:
                                                Does your country border Mexico?
                                                    YES:Belize
                                                    NO:Guyana
                                            NO:
                                                Is dutch the official language in your country?
                                                    YES:Suriname
                                                    NO:Brazil
"""

tree_text3 = """
Is your country in Africa?
    YES:
        Is France your primary European coloniser?
            YES:
                Is Arabic a major language in your country?
                    YES:
                        Does your nation have a Mediterranean Sea coast?
                            YES:
                                Is your nation a monarchy??
                                    YES:Morocco
                                    NO:
                                        Does your nation share a border with 3 or more countries?
                                            YES:Algeria
                                            NO:Tunisia
                            NO:
                                Does your nation have the Indian Ocean coast?
                                    YES:
                                        Is your nation an island?
                                            YES:Comoros
                                            NO:Djibouti
                                    NO:
                                        Is your country landlocked?
                                            YES:Chad
                                            NO:Mauritania
                    NO:
                        Is Christianity the predominant religion?
                            YES:
                                Is your nation categorised as a Central Africal nation?
                                    YES:
                                        Is French the sole official language in your nation?
                                            YES:
                                                Does your nation border 4 or more countries?
                                                    YES:Republic of Congo
                                                    NO:Gabon
                                            NO:
                                                Is your country landlocked?
                                                    YES:Central African Republic
                                                    NO:Cameroon
                                    NO:
                                        Is your nation an island:
                                            YES:Madagascar
                                            NO:
                                                Is your nation a former German colony?
                                                    YES:Togo
                                                    NO:Benin
                            NO:
                                Is your nation landlocked?
                                    YES:
                                        Is your nation one of the largest producer of Uranium?
                                            YES:Niger
                                            NO:
                                                Has your country officially changed its name since independence?
                                                    YES:Burkina Faso
                                                    NO:Mali
                                    NO:
                                        Is your country one of the largest exporters of bauxite?
                                            YES:Guinea
                                            NO:
                                                Is your country the largest producers of cocoa beans?
                                                    YES:Ivory Coast
                                                    NO:Senegal
            NO:
                Is Britain your primary European coloniser?
                    YES:
                        Is your nation landlocked?
                            YES:
                                Is your nation a monarchy?
                                    YES:
                                        Is your nation an enclave?
                                            YES:Lesotho
                                            NO:Eswatini
                                    NO:
                                        Was your nation formerly a part of Rhodesia?
                                            YES:
                                                Does your nation border South Africa?
                                                    YES:Zimbabwe
                                                    NO:Zambia
                                            NO:
                                                Does the River Nile pass through your nation?
                                                    YES:
                                                        Did your country achieve independence in the 21st century?
                                                            YES:South Sudan
                                                            NO:Uganda
                                                    NO:
                                                        Is the Kalahari desert in your country?
                                                            YES:Botswana
                                                            NO:Malawi
                            NO:
                                Is Islam the largest religion in your country?
                                    YES:
                                        Is Arabic the majority language in your nation?
                                            YES:
                                                Does your country have a coast on the Mediterranean Sea?
                                                    YES:Egypt
                                                    NO:Sudan
                                            NO:
                                                Is your nation one of the largest(top 10) based on population?
                                                    YES:Nigeria
                                                    NO:
                                                        Does your country border only one more country?
                                                            YES:The Gambia
                                                            NO:Sierra Leone
                                    NO:
                                        Is your country an island nation?
                                            YES:
                                                Is Hinduism the predominant religion in your nation?
                                                    YES:Mauritius
                                                    NO:Seychelles
                                            NO:
                                                Does your nation have a coast on the Atlantic Ocean?
                                                    YES:
                                                        Does your nation have more than one capital?
                                                            YES:South Africa
                                                            NO:Ghana
                                                    NO:
                                                        Does your country have the tallest mountain in your continent?
                                                            YES:Tanzania
                                                            NO:Kenya
                    NO:
                        Is Portugal your primary European coloniser?
                            YES:
                                Is your nation an island nation?
                                    YES:
                                        Is your nation located in the Gulf of Guinea?
                                            YES:Sao Tome and Principe
                                            NO:Cape Verde
                                    NO:
                                        Is Christianity the major religion in your nation?
                                            YES:Equatorial Guinea
                                            NO:
                                                Does your nation have a Atlantic Ocean coast:
                                                    YES:Angola
                                                    NO:Mozambique
                            NO:
                                Is your nation landlocked?
                                    YES:
                                        Is your nation colonised by Belgium?
                                            YES:
                                                Does your country border 4 or more countries?
                                                    YES:Rwanda
                                                    NO:Burundi
                                            NO:Ethiopia
                                    NO:
                                        Has Italy completely or partially colonised your territory?
                                            YES:
                                                Does your nation have a Mediterranean Sea coast?
                                                    YES:Libya
                                                    NO:
                                                        Is your nation a one-party state?
                                                            YES:Eritrea
                                                            NO:Somalia
                                            NO:
                                                Is English your official language?
                                                    YES:
                                                        Has your nation ever been colonised by a European power?
                                                            YES:Namibia
                                                            NO:Liberia
                                                    NO:
                                                        Was your nation colonised by Belgium?
                                                            YES:Democratic Republic of Congo
                                                            NO:Equatorial Guinea
"""

tree_text_misc = """
Is your country a monarchy?
    YES:
        Does your country have the Union Jack(United Kingdom flag) on top left of its flag?
            YES:
                Is your country one of the largest country(Top 10) in the world?
                    YES:Australia
                    NO:
                        Is your economy the smallest of all UN member nations?
                            YES:Tuvalu
                            NO:New Zealand
            NO:
                Is your country considered a Polynesian country?
                    YES:Tonga
                    NO:
                        Is your country's population greater than 5 million?
                            YES:Papua New Guinea
                            NO:Solomon Islands
    NO:
        Does your country have Compact of Free Association(COFA) with United States?
            YES:
                Is your country exclusively formed from coral atolls and reefs unlike volcanic islands?
                    YES:Marshall Islands
                     NO:
                        Is the deepest point on earth's sea bed located in your country?
                            YES:Federated States of Micronesia
                            NO:Palau
            NO:
                Is your country's population greater than 200,000?
                    YES:
                        Is Hindi an official language in your country?
                            YES:Fiji
                            NO:Vanuatu
                    NO:
                        Is your country generally categorised as Polynesia?
                            YES:Samoa
                            NO:
                                Is your country a single island as opposed to archipelago?
                                    YES:Nauru
                                    NO:Kiribati
"""

# Parse the trees once when the app starts
root1 = parse_tree(tree_text1)
root2 = parse_tree(tree_text2)
root3 = parse_tree(tree_text3)
root_misc = parse_tree(tree_text_misc)

# Store all nodes in the global nodes_dict
store_nodes(root1, nodes_dict)
store_nodes(root2, nodes_dict)
store_nodes(root3, nodes_dict)
store_nodes(root_misc, nodes_dict)

@app.route('/', methods=['GET'])
def home():
    # Render the home page with custom text and a start button
    return render_template('home.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'current_node_id' not in session:
        # Start a new game
        session.clear()
        session['history'] = []  # Initialize history

        # Create a list of root node IDs for the first three trees
        first_roots = [root1.id, root2.id, root3.id]
        random.shuffle(first_roots)
        # Append the miscellaneous root at the end
        first_roots.append(root_misc.id)
        session['root_node_ids'] = first_roots

        # Initialize the index
        session['current_root_index'] = 0

        # Set the current node ID to the first root node ID
        session['current_node_id'] = first_roots[0]

        session.modified = True

    current_node_data = nodes_dict.get(str(session['current_node_id']))

    if current_node_data is None:
        # If session data is corrupted, restart the game
        return redirect(url_for('restart'))

    current_node_text = current_node_data['text']
    yes_node_id = current_node_data['yes']
    no_node_id = current_node_data['no']

    # Check if we have reached a leaf node
    if yes_node_id is None and no_node_id is None:
        if request.method == 'POST':
            # Handle the user's action
            answer = request.form.get('answer')
            if answer == 'BACK':
                # Handle the back action
                if 'history' in session and session['history']:
                    # Go back to the previous node
                    session['current_node_id'] = session['history'].pop()
                    session.modified = True
                    return redirect(url_for('game'))
                else:
                    # No history, go back to home
                    return redirect(url_for('home'))
            else:
                # Invalid input, redirect to game
                return redirect(url_for('game'))
        else:
            # GET request, render the result page
            return render_template('result.html', country=current_node_text)

    if request.method == 'POST':
        # Get the user's answer
        answer = request.form.get('answer')
        if answer == 'BACK':
            # Handle the back action
            if 'history' in session and session['history']:
                # Go back to the previous node
                session['current_node_id'] = session['history'].pop()
                session.modified = True
                return redirect(url_for('game'))
            else:
                # No history, go back to home
                return redirect(url_for('home'))
        elif answer == 'YES':
            # Before moving forward, append current node to history
            if 'history' not in session:
                session['history'] = []
            session['history'].append(session['current_node_id'])
            next_node_id = yes_node_id
            if next_node_id is None:
                # Reached a leaf node
                session.modified = True
                return redirect(url_for('game'))
            else:
                # Update the session with the new node ID
                session['current_node_id'] = next_node_id
                session.modified = True
                return redirect(url_for('game'))
        elif answer == 'NO':
            # Before moving forward, append current node to history
            if 'history' not in session:
                session['history'] = []
            session['history'].append(session['current_node_id'])
            if no_node_id is None:
                # If current node is a head question, move to the next root
                current_root_id = session['root_node_ids'][session['current_root_index']]
                if session['current_node_id'] == current_root_id:
                    session['current_root_index'] += 1
                    if session['current_root_index'] < len(session['root_node_ids']):
                        # Set the current node to the next root
                        session['current_node_id'] = session['root_node_ids'][session['current_root_index']]
                        session.modified = True
                        return redirect(url_for('game'))
                    else:
                        # No more roots to try, handle accordingly
                        session.modified = True
                        return redirect(url_for('game'))
                else:
                    # No 'NO' node, and not at a head question
                    session.modified = True
                    return redirect(url_for('game'))
            else:
                # Update the session with the new node ID
                session['current_node_id'] = no_node_id
                session.modified = True
                return redirect(url_for('game'))
        else:
            # Invalid input, redirect to game
            return redirect(url_for('game'))

    # Display the current question
    return render_template('index.html', question=current_node_text)

@app.route('/restart')
def restart():
    # Clear the session to start a new game
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # For local development only. Render uses the Procfile and WSGI server.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
