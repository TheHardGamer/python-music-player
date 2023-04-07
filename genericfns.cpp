#include "genericfns.hpp"

QStringList genericFns::addSongs()
{
    QStringList files = QFileDialog::getOpenFileNames(nullptr, QObject::tr("Add Songs"), QDir::currentPath(), QObject::tr(""),nullptr, QFileDialog::DontUseNativeDialog);
    for(auto file : files)
    {
        std::cout << "File name : " << file.toStdString();
    }
    return files;
}
