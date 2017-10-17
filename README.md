# Social Recommendation and Personalization Tool

Social Recommendation and Personalization Tool (SRPtool) consists of three main functionalities/mechanisms, as follows:

1. Personalization
2. Relevance Feedback
3. Social Recommendation

Those three main mechanisms are efficiently combined towards delivering personalized information to the end user (either professional or viewer) close to his/her interests, improving end users’ Quality of Experience (QoE) and making the overall PRODUCER toolkit’s usage more appealing. The output of the SRPtool will be the personalized information, which will be offered as appropriately ranked list of multimedia content either to professional users or to the viewers. For the latter, the most relevant content to user’s profile will be ranked higher in the list while for the former higher rank will be assigned to multimedia content that is most relevant to their customers’ characteristics. This personalized information will conclude to significant benefits and profit for the professional users, e.g. production houses, broadcasters, advertising companies, editorial and online publishing companies, etc., as well as it will encourage the usage of the tool by the viewers.

The main goal of personalization mechanism is to effectively and efficiently satisfy individual needs. By considering end users as individuals, implicit characteristics such as personal taste, age, origin, innate needs and experience become important integral parts of system design. In the literature, personalized user interface has been popular by using implicit data captured in user interactions.

The relevance feedback is utilized by the system to learn users’ specific context that they have in mind for the initial streamed video. More specifically, it should be noticed that starting with the same video, two users could end up with very different enrichments and relevant advertisements paired and shown with the video depending on their feedback which contributes to the update of user’s profile. Thus, the main goal of relevance feedback is to learn a model of user’s interest based on his/her interaction sessions with the system.

The general scope of social recommendation mechanism is to collect and analyze different sources of information considering the preferences of the users with respect to a set of items, aiming to provide rankings and scores on these items tailored to each separate user, in order to facilitate the discovery and selection of items by the end user and improve his / her experience.

## To run on your machine

- .env file on root folder
- data_files folder on root folder

## To add your letsencrypt certificate

### To add your letsencrypt certificate

```
docker run -it --rm \
    -v CONTAINERNAME_certs:/etc/letsencrypt \
    -v CONTAINERNAME_certs-data:/data/letsencrypt \
    certbot/certbot \
    certonly \
    --webroot --webroot-path=/data/letsencrypt \
    -d DOMAINNAME.COM -d WWW.DOMAINNAME.COME
```

### To automatically renew your certificate

Add the following cronjob

```
0 0 */15 * * docker run -t --rm -v CONTAINERNAME_certs:/etc/letsencrypt -v CONTAINERNAME_certs-data:/data/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt certbot/certbot renew --webroot --webroot-path=/data/letsencrypt && docker kill -s HUP sptool_webserver_1 >/dev/null 2>&1
```
