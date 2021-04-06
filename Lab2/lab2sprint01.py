import subprocess

comandoCk = """cd C:\ck\target
java -jar ck-0.6.4-SNAPSHOT-jar-with-dependencies.jar C:\java-design-patterns true 0 False"""

subprocess.call("git clone https://github.com/iluwatar/java-design-patterns", shell=True)

subprocess.call(comandoCk, shell=True)


