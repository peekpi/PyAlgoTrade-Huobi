#include <QNetworkRequest>
#include <QCryptographicHash>
#include "quserasset.h"
#include "commfuns.h"

QUserAsset::QUserAsset(QObject *parent) : QObject(parent)
{
    _manager = new QNetworkAccessManager(this);
    connect(_manager, &QNetworkAccessManager::finished, this, &QUserAsset::onFinished);
}

QUserAsset::~QUserAsset()
{
    delete _manager;
}

void QUserAsset::get()
{
    QUrl url(HUOBI_RESTURL);
    QNetworkRequest request(url);

    //set http header
    request.setHeader(QNetworkRequest::ContentTypeHeader, HUOBI_REST_HEADER_CONTENTTYPE);

    QString sData = QString("access_key=%1&created=%2&method=get_account_info").arg(G_Huobi_AccessKey).arg(QDateTime::currentDateTime().toTime_t());
    //calculate sign
    QString sSign = sData + "&secret_key=" + G_Huobi_SecretKey;
    sSign = CommFuns::MD5(sSign);
    sData += "&sign=" + sSign;

    //send request
    _manager->post(request, sData.toUtf8());
}

void QUserAsset::onFinished(QNetworkReply *reply)
{
    if (reply->error() == QNetworkReply::NoError) {
        QByteArray baDatas = reply->readAll();
        //parse to JSON
        QJsonParseError jsonError;
        QJsonDocument jsonDoc = QJsonDocument::fromJson(baDatas, &jsonError);
        if (jsonError.error == QJsonParseError::NoError) {
            this->userAssetInfo = jsonDoc.object();

            //emit signal
            emit updated(this->userAssetInfo);
        }
    } else {
        qDebug() << "QUserAsset::onFinished error" << reply->errorString();
    }

    //release resource
    reply->deleteLater();
}
