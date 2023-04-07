#ifndef GENERIC_FNS_HPP
#define GENERIC_FNS_HPP
#include <cstddef>
#include <iostream>
#include <QMainWindow>
#include <QFileDialog>

class genericFns
{
public:
    genericFns(const genericFns &obj) = delete;
    static genericFns *getInstance()
    {
        if (genericFnsInstance == NULL)
        {
            genericFnsInstance = new genericFns();
            return genericFnsInstance;
        }
        else
        {
            return genericFnsInstance;
        }
    }
    ~genericFns() { delete genericFnsInstance; }
    static QStringList addSongs();
private:
    genericFns(){}
    static genericFns *genericFnsInstance;
};
inline genericFns *genericFns::genericFnsInstance = NULL;
#endif
