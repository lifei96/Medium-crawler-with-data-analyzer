function draw_cc_by_time()
    date_list = {'20120901', '20121001', '20121101', '20121201', '20130101', '20130201', '20130301', '20130401', '20130501', '20130601', '20130701', '20130801', '20130901', '20131001', '20131101', '20131201', '20140101', '20140201', '20140301', '20140401', '20140501', '20140601', '20140701', '20140801', '20140901', '20141001', '20141101', '20141201', '20150101', '20150201', '20150301', '20150401', '20150501', '20150601', '20150701', '20150801', '20150901', '20151001', '20151101', '20151201', '20160101', '20160201', '20160301', '20160401', '20160501', '20160601', '20160701', '20160801'};
    cc_mean = [];
    figure(1);
    for k=1:length(date_list)
        date = date_list{k};
        filepath = strcat('./data/graph/cc_', date, '.csv');
        dataset = csvread(filepath, 1, 1);
        a = dataset(:,1);
        b = a(a<=1 & a>=0);
        cc_mean = [cc_mean mean(b)];
        h = cdfplot(dataset(:,1));
        hold on;
    end
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Clustering Coefficient','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    legend(date_list);
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/graph/CDF_CC_time.eps', '-depsc');
    figure(2);
    dt = datenum(date_list, 'yyyymmdd');
    scatter(dt, cc_mean, '*', 'MarkerEdgeColor', 'k');
    xlim([datenum('08-01-2012') datenum('08-01-2016')]);
    NumTicks = 5;
    L = get(gca,'XLim');
    set(gca,'XTick',linspace(L(1),L(2),NumTicks))
    datetick('x', 'mmm yyyy', 'keeplimits', 'keepticks');
    set(gca, 'FontSize', 12);
    xlabel('','FontSize',20);
    ylabel('Average Clustering Coefficient','FontSize',20);
    title('');
    grid off;
    box on;
    print('./results/graph/CC_time.eps', '-depsc');
end