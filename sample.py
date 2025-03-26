from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/c7e053b04a7e465388c166c779634866"))
address = "0xbfd8137f7d1516D3ea5cA83523914859ec47F573"
ticklens_bytecode = w3.eth.get_code(Web3.to_checksum_address(address)).hex()
ticklens_hash = Web3.keccak(hexstr=ticklens_bytecode).hex()


print(ticklens_bytecode)
