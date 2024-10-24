#include <iostream>
#include <string>
#include<sstream>
#include <fstream>
#include <algorithm>
using namespace std;

// By Atharv :)

string reader(const string&filename, int arg, int arg2, string customurl, int uniquechk, string shorturl){
    ifstream file(filename);
    string line;
    string maxid;
    string id;
    string longUrl; 
    string shortUrl;
    int counter=0;
        while(getline(file, line)){
        stringstream ss(line);    
        getline(ss, longUrl,',');
        getline(ss, shortUrl,',');
        ss>>id;
        maxid= id;
        counter++;
        if (arg2==1 && shorturl==shortUrl){
            return longUrl;
        }
        if (uniquechk==1 && customurl==shortUrl){
            return "not";
        }
        }  
    file.close();
    if (maxid==""){
        maxid="0";
    }
    if (arg==0){
        return maxid;
    }
    else if (arg==1){
        return longUrl;
    }
    else{
        return shortUrl;
    }
}


string urlgen(int id){
    string charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    string base62;
    if (id==0){
        return string(1,charset[0]);
    }
    else{
        int base= charset.length();
        while (id>0){
            int rem= id%base;
            base62+=charset[rem];
            id/=base;
        }
        reverse(base62.begin(), base62.end());
        return base62;
    }
}
void writer(const string&filename, int id, const string&lurl, const string&surl){
    ofstream file;
    file.open(filename, ios_base::app);
    file<<lurl<<","<<surl<<","<<id<<endl;
    file.close();
}

string action(string longurl, int finder){
    int errorCode=0;
    string file_path= "udb.txt";
    int currentId= stoi(reader(file_path,0,-1,"", 0, ""));
    int activeId= currentId+1;
    string userType="Free";
    string customUrl="Testing";
    if (finder==1){
        size_t pos= longurl.find_last_of('/');
        string stripped=longurl.substr(pos +1); 
        return reader(file_path, 0,1,"", 0, stripped);
    }
    else{
        if (userType=="Free"){
        writer(file_path, activeId,longurl, urlgen(activeId));
        return reader(file_path, 2, -1,"",0,"");
    }
    else{
        if (customUrl==""){
            writer(file_path, activeId, longurl, urlgen(activeId));
            string temp=reader(file_path, 2, -1,"",0,"");
            return temp;
        }
        else{
            if(reader(file_path, 0,-1,customUrl,1,"")!="not"){
        writer(file_path, activeId,longurl, customUrl);
        return reader(file_path, 2, -1,"",0,"");
            }
        else{
            string errorCode="1A";
            return errorCode;
            }
        }
    }
    }
}

int main(int argc, char* argv[]){
    string input= argv[1];
    if (input.find("localhost") != string::npos){
        string finalurl= action(input,1);
        cout<<finalurl<<endl;
    }
    else{
        string finalurl=action(input,0);
        cout<<finalurl<<endl;
    }   
    return 0;   
}

