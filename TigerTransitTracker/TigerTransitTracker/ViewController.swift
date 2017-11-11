//
//  ViewController.swift
//  TigerTransitTracker
//
//  Created by Matthew Yeh on 11/11/17.
//  Copyright © 2017 Matthew Yeh. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var webView: UIWebView!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        let myURL = URL(string: "http://www.google.com")
        let myURLRequest = URLRequest(url: myURL!)
        webView.loadRequest(myURLRequest)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

