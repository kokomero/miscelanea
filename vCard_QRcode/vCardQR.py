import urllib2
import qrcode

#Get the vCard from an URL
vcf_file = urllib2.urlopen('http://www.victormontielargaiz.net/victor.vcf')
vcard = vcf_file.read()
vcf_file.close()

#Create a QRCode object
qr = qrcode.QRCode(version=20, error_correction=ERROR_CORRECT_M)
#Choose the best size for the text to be encoded
qr.best_fit(start=None) 
#Add the text to be encoded and generate QRCode
qr.add_data( vcard )
qr.make() 

#im contains a PIL.Image.Image object
im = qr.make_image()

#Save it to a file
im.save("/tmp/vCard_QR.png")