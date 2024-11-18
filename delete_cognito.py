import boto3

# Initialize the Cognito client
cognito_client = boto3.client('cognito-idp', region_name='us-east-1')

# Look up the user pool details
def get_user_pool_id(pool_name):
    try:
        response = cognito_client.list_user_pools(MaxResults=50)
        for pool in response['UserPools']:
            if pool['Name'] == pool_name:
                return pool['Id']
        raise ValueError(f"User pool with name '{pool_name}' not found.")
    except Exception as e:
        print(f"Error retrieving user pool ID: {e}")
        return None

# Look up app client ID
def get_app_client_id(user_pool_id):
    try:
        response = cognito_client.list_user_pool_clients(UserPoolId=user_pool_id, MaxResults=50)
        if response['UserPoolClients']:
            return response['UserPoolClients'][0]['ClientId']  # Assumes only one app client exists
        raise ValueError("No app client found for the user pool.")
    except Exception as e:
        print(f"Error retrieving app client ID: {e}")
        return None

# Look up hosted UI domain
def get_hosted_ui_domain(user_pool_id):
    try:
        response = cognito_client.describe_user_pool(UserPoolId=user_pool_id)
        return response['UserPool']['Domain'] if 'Domain' in response['UserPool'] else None
    except Exception as e:
        print(f"Error retrieving hosted UI domain: {e}")
        return None

# Look up resource server identifier
def get_resource_server_identifier(user_pool_id):
    try:
        response = cognito_client.list_resource_servers(UserPoolId=user_pool_id, MaxResults=50)
        if response['ResourceServers']:
            return response['ResourceServers'][0]['Identifier']  # Assumes only one resource server exists
        raise ValueError("No resource server found for the user pool.")
    except Exception as e:
        print(f"Error retrieving resource server identifier: {e}")
        return None

# Delete the App Client
def delete_app_client(user_pool_id, app_client_id):
    try:
        cognito_client.delete_user_pool_client(UserPoolId=user_pool_id, ClientId=app_client_id)
        print(f"Deleted App Client: {app_client_id}")
    except Exception as e:
        print(f"Error deleting App Client: {e}")

# Delete the Resource Server
def delete_resource_server(user_pool_id, resource_server_identifier):
    try:
        cognito_client.delete_resource_server(
            UserPoolId=user_pool_id,
            Identifier=resource_server_identifier
        )
        print(f"Deleted Resource Server: {resource_server_identifier}")
    except Exception as e:
        print(f"Error deleting Resource Server: {e}")

# Delete the Hosted UI domain
def delete_hosted_ui_domain(user_pool_id, domain_name):
    try:
        cognito_client.delete_user_pool_domain(
            UserPoolId=user_pool_id,
            Domain=domain_name
        )
        print(f"Deleted Hosted UI domain: {domain_name}")
    except Exception as e:
        print(f"Error deleting Hosted UI domain: {e}")

# Delete the User Pool
def delete_user_pool(user_pool_id):
    try:
        cognito_client.delete_user_pool(UserPoolId=user_pool_id)
        print(f"Deleted User Pool: {user_pool_id}")
    except Exception as e:
        print(f"Error deleting User Pool: {e}")

# Main execution
if __name__ == "__main__":
    pool_name = 'the_cafe'

    # Look up resources
    user_pool_id = get_user_pool_id(pool_name)
    if user_pool_id:
        app_client_id = get_app_client_id(user_pool_id)
        domain_name = get_hosted_ui_domain(user_pool_id)
        resource_server_identifier = get_resource_server_identifier(user_pool_id)

        # Delete resources
        if app_client_id:
            delete_app_client(user_pool_id, app_client_id)
        if resource_server_identifier:
            delete_resource_server(user_pool_id, resource_server_identifier)
        if domain_name:
            delete_hosted_ui_domain(user_pool_id, domain_name)
        delete_user_pool(user_pool_id)
