//
//  DetailViewController.h
//  address book
//
//  Created by mhci on 2015/7/9.
//  Copyright © 2015年 mhci. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DetailViewController : UIViewController

@property (strong, nonatomic) id detailItem;
@property (weak, nonatomic) IBOutlet UILabel *detailDescriptionLabel;

@end

