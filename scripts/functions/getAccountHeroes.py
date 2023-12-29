import requests
graph_url = "https://api.defikingdoms.com/graphql"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

def getAccountHeroes(user, network):
    query = """
            query ($user: String, $network: String) {
                heroes(where: {owner: $user, network: $network}) {
                    id
                    xp
                    level
                    generation
                    summons
                    maxSummons
                    mainClass
                    subClass
                    currentQuest
                    saleAuction {
                        id
                    }
                }
            }
        """
    variables = {
            "user": user,
            "network": network
        }

    response = requests.post(
            graph_url, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code != 200:
        print("Error fetching account heroes")
        return []
    
    return response.json()["data"]["heroes"]


def getAccountHeroesByClass(user, network, mainClasses):
    query = """
            query ($user: String, $network: String, $classes: [Int]) {
                heroes(where: {owner: $user, network: $network, mainClass_in: $classes}) {
                    id
                    xp
                    level
                    generation
                    summons
                    maxSummons
                    mainClass
                    subClass
                    currentQuest
                    saleAuction {
                        id
                    }
                }
            }
        """
    variables = {
            "user": user,
            "network": network,
            "classes": mainClasses
        }

    response = requests.post(
            graph_url, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code != 200:
        print("Error fetching account heroes")
        return []
    
    return response.json()["data"]["heroes"]